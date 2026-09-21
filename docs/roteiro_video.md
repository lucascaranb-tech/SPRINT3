# 🎥 Roteiro do vídeo — Sprint 3

**Duração sugerida:** 3min30s a 4min30s.

A ideia é não ficar lendo o README. O vídeo deve mostrar a aplicação funcionando e, enquanto a tela muda, explicar o que está acontecendo.

---

## 0:00–0:20 — Abertura

### Na tela
Mostrar o GitHub rapidamente ou a página inicial do projeto.

### Fala
> "Olá, somos a equipe do ChargeGrid Intelligence. Nesta Sprint 3 vamos demonstrar o protótipo funcional da nossa solução para gerenciamento inteligente de recarga comercial de veículos elétricos. Vamos mostrar como os dados dos veículos entram no sistema, como a demanda é calculada, como a potência é distribuída e como o sistema gera uma decisão operacional."

---

## 0:20–0:50 — Contexto

### Na tela
Abrir o `README.md` ou `docs/arquitetura.md` e mostrar rapidamente o diagrama.

### Fala
> "A proposta surgiu dos problemas identificados nas etapas anteriores, principalmente sobrecarga em horários de pico, dificuldade de cobrança, falta de padronização e uso ineficiente da energia. Na Sprint 2 já tínhamos uma simulação funcional. Agora transformamos essa lógica em uma demonstração integrada, com comandos de operação e registro dos eventos."

---

## 0:50–1:30 — Abrindo a aplicação

### Onde ir
No terminal, dentro da pasta do projeto:

```bash
streamlit run app.py
```

Depois abra:

```text
http://localhost:8501
```

### Fala
> "Aqui temos o nosso dashboard. Na lateral podemos configurar a potência disponível do eletroposto, o período da recarga, o preço base e os veículos conectados."

### Faça
Mostre a lateral e passe rapidamente por:
- potência;
- horário;
- preço;
- veículos;
- bateria;
- potência solicitada;
- conector;
- pagamento.

---

## 1:30–2:15 — Demonstrando o problema de demanda

### Faça
1. Deixe a potência disponível em **60 kW**.
2. Coloque 4 veículos.
3. Deixe as potências solicitadas próximas de 22 kW.
4. Use **Horário de pico**.
5. Deixe pelo menos um pagamento aprovado.

### Fala
> "Neste cenário temos vários veículos solicitando recarga ao mesmo tempo. O sistema soma a potência solicitada pelos veículos aprovados e calcula o percentual de utilização da infraestrutura. Como estamos simulando um horário de pico, a tarifa também pode ser ajustada."

### Mostre
Os quatro cards:
- potência disponível;
- potência solicitada;
- uso da infraestrutura;
- tarifa dinâmica.

---

## 2:15–2:55 — Balanceamento e decisão

### Faça
Clique em:

**Rebalancear potência**

### Fala
> "Agora vamos executar o comando de rebalanceamento. O motor de decisão considera o status de pagamento e a prioridade relacionada ao nível de bateria para distribuir a potência disponível entre as sessões autorizadas."

### Mostre
A tabela de sessões e compare:
- potência solicitada;
- potência alocada;
- prioridade;
- status.

---

## 2:55–3:30 — Pagamento e integração

### Faça
Altere um veículo de **Pendente** para **Aprovado**.

Depois clique novamente em:

**Rebalancear potência**

### Fala
> "Agora vamos aprovar uma sessão que estava pendente. Ao executar novamente o processamento, essa sessão passa a participar da distribuição de potência. Isso demonstra a integração entre pagamento, controle de demanda e operação."

### Mostre
A tabela atualizada.

---

## 3:30–4:00 — Gráfico e eventos

### Faça
Role para baixo.

### Mostre
- gráfico de distribuição;
- interoperabilidade;
- eventos recentes.

### Fala
> "Além da tabela, o sistema apresenta visualmente a distribuição de potência e registra os eventos da operação. A estrutura dos dados também mantém informações padronizadas de veículo, conector, potência, pagamento, status e custo, representando a camada de interoperabilidade."

---

## 4:00–4:20 — Fechamento

### Fala
> "Com isso demonstramos a integração dos principais componentes da solução: entrada dos dados, processamento da demanda, balanceamento de potência, tarifação, status de pagamento e decisão inteligente. O protótipo evidencia como esses componentes podem trabalhar juntos em uma operação comercial de recarga."

> "Obrigado."

---

# ✅ Checklist antes de gravar

- [ ] `pip install -r requirements.txt`
- [ ] `streamlit run app.py`
- [ ] Navegador aberto no localhost
- [ ] Potência em 60 kW
- [ ] 4 veículos
- [ ] Horário de pico
- [ ] Pelo menos 1 pagamento pendente
- [ ] Pelo menos 1 pagamento aprovado
- [ ] Gravar primeiro o cenário inicial
- [ ] Clicar em "Rebalancear potência"
- [ ] Aprovar uma sessão
- [ ] Rebalancear novamente
- [ ] Mostrar gráfico
- [ ] Mostrar eventos
- [ ] Encerrar com a integração dos componentes

# 🎙️ Dica para falar

Não precisa decorar palavra por palavra. Usem as frases como guia e falem olhando para o que está aparecendo na tela. O mais importante é explicar **o que mudou e por que o sistema tomou aquela decisão**.