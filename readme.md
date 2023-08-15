# Análise de Sinais de Compra e Venda usando RSI

Este é um projeto de análise de sinais de compra e venda utilizando o Índice de Força Relativa (RSI) em Python. O objetivo é identificar oportunidades de compra e venda com base nas variações de preço de um ativo financeiro.

## Descrição

Este projeto utiliza a biblioteca Pandas, yfinance e Matplotlib para baixar dados históricos de um ativo escolhido e calcular o RSI. O RSI é um indicador que ajuda a avaliar se um ativo está sobrecomprado ou sobrevendido. Com base no RSI, são gerados sinais de compra e venda, e é calculada a performance das operações.

## Funcionalidades

- Baixar dados históricos de um ativo financeiro através do Yahoo Finance.
- Calcular o RSI e identificar sinais de compra e venda.
- Apresentar gráficos destacando as datas de compra e venda.
- Calcular a performance das operações.

## Como Usar

1. Instale as bibliotecas necessárias: Pandas, yfinance e Matplotlib.
2. Escolha o ativo de interesse no código, por exemplo: `ativo = 'PETR4.SA'`.
3. Execute o código Python.
4. Visualize os resultados, incluindo gráficos de compra e venda e análise de performance.

## Exemplo de Uso

```python
# Definir o ativo de interesse
ativo = 'PETR4.SA'

# Baixar e analisar os dados do ativo
# ...

# Identificar datas de compra e venda
# ...

# Calcular e imprimir a performance das operações
# ...
