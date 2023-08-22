'''
Análise Financeira usando Estratégia de RSI
Este código realiza uma análise técnica de um ativo escolhido, usando o Índice de Força Relativa (RSI) como base.
Ele baixa os dados do ativo, calcula os retornos, identifica sinais de compra e venda com base no RSI,
calcula lucros obtidos e analisa o desempenho da estratégia.
Certifique-se de ajustar o ativo e os parâmetros conforme necessário.
Lembre-se de que resultados passados podem não garantir resultados futuros.
Autor: Alexandre Lo Bianco
Data: 22/08/2023
Referencia: Varos Programação
'''


# 1- Importa as bibliotecas necessárias: pandas, yfinance, matplotlib e numpy.
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Configuração para suprimir advertências de atribuição encadeada
pd.options.mode.chained_assignment = None


# 2 - Define o ativo a ser analisado 
#  Pesquise nomes de ativos em https://finance.yahoo.com/
#  ex.: 'PETR4.SA', 'PETR3.SA', 'VALE3.SA', 'MGLU3.SA', 'ITUB4.SA', 'GC=F', 'WEGE3.SA', 'ABEV3.SA', 'AERI3.SA', 'CIEL3.SA','PRIO3.SA', 'BBSE3.SA','HYPE3.SA','ASAI3.SA','SBSP3.SA','CPLE6.SA','ELET6.SA'
ativo = 'PETR4.SA'


# 3 - Faz o download dos dados do ativo escolhido através da biblioteca yfinance.
#  O intervalo de datas deve começar após a data em que o ativo começou a ser negociado para evitar erros.
dados_ativo = yf.download(ativo)


# 4 - VERIFICAR CONSISTÊNCIA DOS DADOS
# Caso a data de início do ativo seja inferior a data em que o ativo começou a ser negociado, a variavel dados_ativo, deve ser ediata com o comando: 
# dados_ativo = yf.download(ativo, start='2021-01-01', end='2021-12-31')
dados_ativo['Adj Close'].plot()
plt.show()

# 5 - Tratamento de retornos. remove os valores nulos e calcula os retornos.
dados_ativo['retornos'] = dados_ativo['Adj Close'].pct_change().dropna()

# 6- Classifica retornos positivos e negativos.
dados_ativo['retornos_positivos'] = dados_ativo['retornos'].apply(lambda x: x if x > 0 else 0)
dados_ativo['retornos_negativos'] = dados_ativo['retornos'].apply(lambda x: abs(x) if x < 0 else 0)
dados_ativo = dados_ativo.dropna()

# 7 - Calcula média de 22 dias de retornos positivos e negativos.
dados_ativo['media_retornos_positivos'] = dados_ativo['retornos_positivos'].rolling(window=22).mean()
dados_ativo['media_retornos_negativos'] = dados_ativo['retornos_negativos'].rolling(window=22).mean()
dados_ativo = dados_ativo.dropna()

# 8 - Calcula índice de força relativa (RSI)
dados_ativo['RSI'] = (100 - 100 / (1 + dados_ativo['media_retornos_positivos'] / dados_ativo['media_retornos_negativos']))

# 9 - Sinaliza como compra ou venda
dados_ativo.loc[dados_ativo['RSI'] < 30, 'compra'] = 'sim'
dados_ativo.loc[dados_ativo['RSI'] > 30, 'compra'] = 'nao'

# 10 - Modelo simplificado de compra

datas_compra = []

for i in range(len(dados_ativo)):
    if "sim" in dados_ativo['compra'].iloc[i]:
        datas_compra.append(dados_ativo.index[i + 1])

# 11 - Modelo avançado de compra e venda

data_compra = []
data_venda = []

for i in range(len(dados_ativo)):
    if "sim" in dados_ativo['compra'].iloc[i]:
        data_compra.append(dados_ativo.index[i + 1])
        
        for j in range(1, 11):
            if dados_ativo['RSI'].iloc[i + j] > 40:
                data_venda.append(dados_ativo.index[i + j + 1])
                break
            elif j == 10:
                data_venda.append(dados_ativo.index[i + j + 1])

# 12 - Análise dos graficos gerados
plt.figure(figsize=(12, 5))
plt.scatter(dados_ativo.loc[data_compra].index, dados_ativo.loc[data_compra]['Adj Close'], marker='^', c='g')
plt.scatter(dados_ativo.loc[data_venda].index, dados_ativo.loc[data_venda]['Adj Close'], marker='v', c='r', label='Venda')
plt.plot(dados_ativo['Adj Close'], alpha=0.7)
plt.show()

# 13 - Calculo dos lucros
lucros = dados_ativo.loc[data_venda]['Open'].values / dados_ativo.loc[data_compra]['Open'].values - 1

# 14 - Resultados dos lucros
operacoes_vencedoras = len(lucros[lucros > 0]) / len(lucros)
media_ganhos = np.mean(lucros[lucros > 0])
media_perdas = abs(np.mean(lucros[lucros < 0]))
expectativa_matematica_modelo = (operacoes_vencedoras * media_ganhos) - ((1 - operacoes_vencedoras) * media_perdas)
performance_acumulada = (np.cumprod((1 + lucros)) - 1)
retorno_buy_and_hold = dados_ativo['Adj Close'].iloc[-1] / dados_ativo['Adj Close'].iloc[0] - 1

print(f"Operações Vencedoras: {operacoes_vencedoras}")
print(f"Média de Ganhos: {media_ganhos * 100:.2f}%")
print(f"Média de Perdas: {media_perdas * 100:.2f}%")
print(f"Expectativa Matemática do Modelo: {expectativa_matematica_modelo * 100:.2f}%")
print(f"Performance Acumulada: {performance_acumulada[-1] * 100:.2f}%")
print(f"Retorno Buy and Hold: {retorno_buy_and_hold * 100:.2f}%")

