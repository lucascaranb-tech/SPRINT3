import random
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ChargeGrid Intelligence — Sprint 3",
    page_icon="⚡",
    layout="wide",
)

def calcular_prioridade(bateria_atual: int, pagamento: str) -> int:
    if pagamento != "Aprovado":
        return 0
    if bateria_atual <= 20:
        return 3
    if bateria_atual <= 50:
        return 2
    return 1

def calcular_tarifa(preco_base: float, horario: str, uso_percentual: float) -> float:
    multiplicador = 1.0
    if horario == "Intermediário":
        multiplicador += 0.15
    elif horario == "Horário de pico":
        multiplicador += 0.35
    if uso_percentual >= 90:
        multiplicador += 0.25
    elif uso_percentual >= 70:
        multiplicador += 0.15
    return round(preco_base * multiplicador, 2)

def classificar_demanda(uso_percentual: float) -> str:
    if uso_percentual >= 90:
        return "Alta"
    if uso_percentual >= 70:
        return "Média"
    return "Baixa"

def gerar_recomendacao(demanda: str, pendentes: int, recusados: int) -> str:
    if recusados > 0:
        return "Bloquear sessões com pagamento recusado e liberar potência para veículos aprovados."
    if pendentes > 0:
        return "Manter veículos pendentes em espera até confirmação do pagamento."
    if demanda == "Alta":
        return "Ativar controle de carga inteligente e priorizar veículos com bateria crítica."
    if demanda == "Média":
        return "Distribuir potência de forma equilibrada e monitorar aumento de demanda."
    return "Operação normal. Há potência suficiente para atender as sessões ativas."

def processar_sessoes(veiculos, potencia_total, preco_base, horario):
    df = pd.DataFrame(veiculos)
    if df.empty:
        return df, 0, 0, 0, "Baixa", 0.0, "Sem sessões."

    df["prioridade"] = df.apply(
        lambda row: calcular_prioridade(row["bateria_atual"], row["pagamento"]),
        axis=1,
    )
    df_aprovados = df[df["pagamento"] == "Aprovado"].copy()
    df_bloqueados = df[df["pagamento"] != "Aprovado"].copy()

    potencia_total_solicitada = (
        int(df_aprovados["potencia_solicitada"].sum())
        if not df_aprovados.empty else 0
    )
    uso_percentual = (
        min((potencia_total_solicitada / potencia_total) * 100, 100)
        if potencia_total > 0 else 0
    )
    tarifa = calcular_tarifa(preco_base, horario, uso_percentual)
    demanda = classificar_demanda(uso_percentual)

    if not df_aprovados.empty:
        df_aprovados = df_aprovados.sort_values(
            by=["prioridade", "bateria_atual"],
            ascending=[False, True],
        )
        soma_pesos = df_aprovados["prioridade"].sum()
        if soma_pesos == 0:
            df_aprovados["potencia_alocada"] = 0.0
        else:
            df_aprovados["potencia_alocada"] = df_aprovados.apply(
                lambda row: min(
                    row["potencia_solicitada"],
                    round((row["prioridade"] / soma_pesos) * potencia_total, 2),
                ),
                axis=1,
            )
            excesso = df_aprovados["potencia_alocada"].sum() - potencia_total
            if excesso > 0:
                idx = df_aprovados["potencia_alocada"].idxmax()
                df_aprovados.loc[idx, "potencia_alocada"] = max(
                    0,
                    round(df_aprovados.loc[idx, "potencia_alocada"] - excesso, 2),
                )
    else:
        df_aprovados["potencia_alocada"] = pd.Series(dtype=float)

    if not df_bloqueados.empty:
        df_bloqueados["potencia_alocada"] = 0.0

    resultado = pd.concat([df_aprovados, df_bloqueados], ignore_index=True)
    resultado["energia_necessaria_kWh"] = (
        (resultado["bateria_desejada"] - resultado["bateria_atual"]) * 0.6
    ).round(2)
    resultado["custo_estimado_R$"] = (
        resultado["energia_necessaria_kWh"] * tarifa
    ).round(2)
    resultado["status_sessao"] = resultado["pagamento"].apply(
        lambda p: (
            "Recarga autorizada" if p == "Aprovado"
            else "Aguardando pagamento" if p == "Pendente"
            else "Bloqueada"
        )
    )
    recomendacao = gerar_recomendacao(
        demanda,
        int((resultado["pagamento"] == "Pendente").sum()),
        int((resultado["pagamento"] == "Recusado").sum()),
    )
    return (
        resultado,
        potencia_total_solicitada,
        uso_percentual,
        tarifa,
        demanda,
        float(resultado["potencia_alocada"].sum()),
        recomendacao,
    )

if "eventos" not in st.session_state:
    st.session_state.eventos = []
if "ultima_acao" not in st.session_state:
    st.session_state.ultima_acao = "Nenhum comando executado ainda."

def registrar_evento(mensagem: str):
    st.session_state.eventos.insert(
        0,
        {"horario": datetime.now().strftime("%H:%M:%S"), "evento": mensagem},
    )
    st.session_state.eventos = st.session_state.eventos[:10]

st.title("⚡ ChargeGrid Intelligence")
st.subheader("Sprint 3 — Prototipagem Funcional e Integração")
st.write(
    "Protótipo funcional para demonstrar a integração entre controle de demanda, "
    "tarifação, pagamento, interoperabilidade e decisão inteligente."
)

st.sidebar.header("Configuração do eletroposto")
potencia_total = st.sidebar.slider(
    "Potência total disponível (kW)", 20, 150, 60, 5
)
horario = st.sidebar.selectbox(
    "Período da recarga", ["Fora de pico", "Intermediário", "Horário de pico"]
)
preco_base = st.sidebar.number_input(
    "Preço base por kWh (R$)", 0.50, 5.00, 1.60, 0.10
)
st.sidebar.markdown("---")
st.sidebar.header("Veículos conectados")
quantidade_veiculos = st.sidebar.slider(
    "Quantidade de veículos", 1, 6, 4, 1
)

veiculos = []
for i in range(1, quantidade_veiculos + 1):
    with st.sidebar.expander(f"Veículo {i}", expanded=i <= 3):
        bateria_atual = st.slider(
            f"Bateria atual V{i} (%)", 5, 95, max(10, 70 - i * 12), 5,
            key=f"bateria_{i}",
        )
        bateria_desejada = st.slider(
            f"Bateria desejada V{i} (%)",
            min(bateria_atual + 5, 100), 100,
            min(max(bateria_atual + 20, 60), 100), 5,
            key=f"desejada_{i}",
        )
        potencia_solicitada = st.slider(
            f"Potência solicitada V{i} (kW)", 3, 50, 22, 1,
            key=f"potencia_{i}",
        )
        conector = st.selectbox(
            f"Tipo de conector V{i}", ["Tipo 2", "CCS2", "CHAdeMO"],
            key=f"conector_{i}",
        )
        pagamento = st.selectbox(
            f"Pagamento V{i}", ["Aprovado", "Pendente", "Recusado"],
            key=f"pagamento_{i}",
        )
        veiculos.append({
            "veiculo": f"EV-{i:03d}",
            "bateria_atual": bateria_atual,
            "bateria_desejada": bateria_desejada,
            "potencia_solicitada": potencia_solicitada,
            "conector": conector,
            "pagamento": pagamento,
        })

(
    resultado, potencia_total_solicitada, uso_percentual, tarifa,
    demanda, potencia_alocada_total, recomendacao,
) = processar_sessoes(veiculos, potencia_total, preco_base, horario)

st.markdown("### Comandos de operação")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔄 Rebalancear potência", use_container_width=True):
        st.session_state.ultima_acao = (
            f"Rebalanceamento executado às {datetime.now().strftime('%H:%M:%S')}."
        )
        registrar_evento(
            f"Rebalanceamento: {potencia_alocada_total:.1f} kW distribuídos."
        )
        st.rerun()
with c2:
    if st.button("▶️ Iniciar nova sessão", use_container_width=True):
        registrar_evento("Nova sessão simulada: dados processados pelo motor de decisão.")
        st.session_state.ultima_acao = (
            f"Nova sessão processada às {datetime.now().strftime('%H:%M:%S')}."
        )
        st.rerun()
with c3:
    if st.button("🧹 Limpar histórico", use_container_width=True):
        st.session_state.eventos = []
        st.session_state.ultima_acao = "Histórico de eventos limpo."
        st.rerun()

st.info(f"Última ação: {st.session_state.ultima_acao}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Potência disponível", f"{potencia_total} kW")
m2.metric("Potência solicitada", f"{potencia_total_solicitada} kW")
m3.metric("Uso da infraestrutura", f"{uso_percentual:.1f}%")
m4.metric("Tarifa dinâmica", f"R$ {tarifa:.2f}/kWh")
st.markdown("---")

col_a, col_b = st.columns([2.1, 1])
with col_a:
    st.subheader("Sessões de recarga")
    colunas = [
        "veiculo", "conector", "bateria_atual", "bateria_desejada",
        "pagamento", "prioridade", "potencia_solicitada",
        "potencia_alocada", "energia_necessaria_kWh",
        "custo_estimado_R$", "status_sessao",
    ]
    st.dataframe(resultado[colunas], use_container_width=True, hide_index=True)

with col_b:
    st.subheader("Decisão inteligente")
    if demanda == "Alta":
        st.error(f"Demanda atual: {demanda}")
    elif demanda == "Média":
        st.warning(f"Demanda atual: {demanda}")
    else:
        st.success(f"Demanda atual: {demanda}")
    st.write(recomendacao)
    st.markdown("**Integração simulada**")
    st.write("1. Entrada dos veículos")
    st.write("2. Motor de decisão")
    st.write("3. Controle de potência")
    st.write("4. Tarifação")
    st.write("5. Resultado no dashboard")

st.markdown("---")
st.subheader("Distribuição de potência")
grafico = resultado[["veiculo", "potencia_solicitada", "potencia_alocada"]].set_index("veiculo")
st.bar_chart(grafico)

c3, c4 = st.columns(2)
with c3:
    st.subheader("Interoperabilidade")
    st.write(
        "Cada sessão mantém uma estrutura padronizada com veículo, conector, "
        "potência solicitada, potência alocada, pagamento, status e custo."
    )
with c4:
    st.subheader("Eventos recentes")
    if st.session_state.eventos:
        st.dataframe(
            pd.DataFrame(st.session_state.eventos),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("Execute um dos comandos acima para gerar eventos.")

st.markdown("---")
st.subheader("Resumo técnico")
st.write(
    "A Sprint 3 transforma a lógica da Sprint 2 em uma demonstração integrada: "
    "o operador altera as condições do eletroposto, o sistema recalcula a demanda, "
    "redistribui potência, calcula a tarifa, verifica o pagamento e apresenta uma "
    "recomendação de operação."
)
