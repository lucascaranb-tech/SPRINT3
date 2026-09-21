# ⚡ ChargeGrid Intelligence — Sprint 3

**FIAP + GoodWe Challenge 2026**

Protótipo funcional de gerenciamento inteligente de recarga comercial de veículos elétricos.

> **Sprint 3 — Prototipagem Funcional e Integração**

## 👥 Equipe

| Integrante | RM |
|---|---:|
| Mauricio Bertuci Saletti | RM571229 |
| Lucas Caram Bueno | RM570158 |
| Rhuan Pacheco Carreri | RM570129 |
| Leonardo Fortini Marcelo | RM572566 |
| Nicolas Andrade Rodrigues | RM572782 |

## 🎯 Objetivo

O ChargeGrid Intelligence propõe uma solução para a expansão da recarga de veículos elétricos do ambiente residencial para o comercial. O projeto trabalha com quatro pilares: **controle de demanda, protocolos abertos, tarifação/pagamento e inteligência artificial**.

Na Sprint 2, a equipe já possuía uma prova de conceito em Streamlit capaz de simular veículos, limitar a potência disponível, priorizar sessões, calcular tarifa dinâmica, simular pagamento e gerar uma recomendação baseada em regras.

Nesta Sprint 3, essa lógica foi organizada em um protótipo integrado com **comandos de operação, processamento das sessões, redistribuição de potência, indicadores, gráfico, eventos e documentação técnica**.

## 🔌 O que o protótipo demonstra

1. Cadastro/simulação de veículos conectados.
2. Limite de potência disponível no eletroposto.
3. Priorização por nível de bateria e pagamento.
4. Balanceamento de potência.
5. Tarifação dinâmica conforme horário e utilização.
6. Status de pagamento e sessão.
7. Recomendação automática de operação.
8. Padronização dos dados das sessões.
9. Comandos simulados de operação.
10. Registro de eventos recentes.

## 🧠 Fluxo integrado

```text
┌─────────────────────┐
│ Veículos / Usuários │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Dashboard Streamlit │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Motor de decisão    │
│ - prioridade        │
│ - demanda           │
│ - pagamento         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Balanceamento       │
│ de potência         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Tarifação + status  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Resultado + eventos │
└─────────────────────┘
```

## 🏗️ Arquitetura

```text
ENTRADA
  │
  ├── Potência disponível
  ├── Horário
  ├── Preço base
  └── Dados dos veículos
          │
          ▼
PROCESSAMENTO
  │
  ├── Validação de pagamento
  ├── Cálculo de prioridade
  ├── Classificação da demanda
  ├── Tarifação dinâmica
  └── Balanceamento de potência
          │
          ▼
SAÍDA
  │
  ├── Potência alocada
  ├── Custo estimado
  ├── Status da sessão
  ├── Recomendação
  └── Eventos da operação
```

## 🧩 Relação com a proposta das Sprints anteriores

O material conceitual do projeto identifica cinco problemas na recarga comercial: sobrecarga em horários de pico, falta de padronização, dificuldade de cobrança, experiência do usuário e ineficiência energética. A proposta apresenta como respostas o balanceamento dinâmico, a plataforma digital e os protocolos abertos.

A aplicação prática desta Sprint 3 concentra-se principalmente em **controle de demanda, tarifação, pagamento, interoperabilidade e decisão inteligente**.

## 💻 Tecnologias

- Python 3
- Streamlit
- Pandas
- GitHub

## ▶️ Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/lucascaranb-tech/chargegrid-intelligence-sprint3.git
cd chargegrid-intelligence-sprint3
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar

```bash
streamlit run app.py
```

### 4. Abrir no navegador

Normalmente:

```text
http://localhost:8501
```

## 🎥 Demonstração

**Vídeo YouTube:** [INSERIR LINK DO VÍDEO NÃO LISTADO]

## 📚 Documentação

- `docs/arquitetura.md` — arquitetura e integração.
- `docs/roteiro_video.md` — roteiro de gravação com falas e ações na tela.
- `docs/dados_exemplo_sessoes.csv` — dados de exemplo.
- `Entrega_FIAP_Sprint3.txt` — arquivo solicitado para entrega.

## 🔗 Repositório da Sprint 2

https://github.com/MauricioBertuci/chargegrid-intelligence-sprint2

## 📌 Observação sobre a IA

Nesta prova de conceito, a "inteligência" é representada por **regras de decisão** baseadas nos dados simulados: nível de bateria, pagamento e demanda. O objetivo da demonstração é evidenciar a integração funcional e o fluxo de decisão, sem apresentar a lógica de regras como um modelo de machine learning treinado.

## 📖 Referência conceitual

O projeto conceitual descreve a IA como responsável por analisar padrões de uso, prever picos de demanda e otimizar a distribuição de energia. A Sprint 3 apresenta a camada funcional simulada que representa parte desse fluxo em operação.
