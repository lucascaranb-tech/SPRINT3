# Arquitetura — Sprint 3

## 1. Visão geral

A Sprint 3 integra a lógica desenvolvida anteriormente em um protótipo único. O operador altera as condições do eletroposto e os dados dos veículos; o sistema processa essas entradas e apresenta o resultado da decisão.

## 2. Componentes

### Entrada
- Potência total disponível.
- Período da recarga.
- Preço base.
- Quantidade de veículos.
- Bateria atual/desejada.
- Potência solicitada.
- Tipo de conector.
- Status de pagamento.

### Motor de decisão
- Cálculo de prioridade.
- Classificação da demanda.
- Tarifação dinâmica.
- Verificação de pagamentos.
- Distribuição de potência.
- Geração de recomendação.

### Saída
- Potência solicitada.
- Potência alocada.
- Percentual de utilização.
- Tarifa dinâmica.
- Energia necessária.
- Custo estimado.
- Status da sessão.
- Recomendação.
- Histórico de eventos.

## 3. Integração demonstrada

```text
Dados simulados
      ↓
DataFrame/Pandas
      ↓
Regras do ChargeGrid
      ↓
Balanceamento de potência
      ↓
Tarifação
      ↓
Decisão operacional
      ↓
Dashboard + gráfico + eventos
```

## 4. Interoperabilidade

A aplicação mantém campos padronizados por sessão:

`veiculo`, `conector`, `potencia_solicitada`, `potencia_alocada`, `pagamento`, `status_sessao` e `custo_estimado_R$`.

Isso representa a camada de dados necessária para que equipamentos e plataformas possam trocar informações de maneira estruturada.

## 5. Cenário recomendado para a demonstração

Use inicialmente:
- Potência disponível: **60 kW**
- 4 veículos
- Horário: **Horário de pico**
- Pagamento: pelo menos 1 veículo como **Aprovado** e 1 como **Pendente** ou **Recusado**

Depois:
1. mostre o dashboard;
2. aumente a potência solicitada;
3. execute **Rebalancear potência**;
4. altere um pagamento para **Aprovado**;
5. execute novamente;
6. mostre a mudança nos dados e nos eventos.