import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Configuração para suprimir advertências de atribuição encadeada
pd.options.mode.chained_assignment = None

'''
1. ESCOLHER O ATIVO
   Pesquise nomes de ativos em https://finance.yahoo.com/
   ex.: 'PETR4.SA', 'PETR3.SA', 'VALE3.SA', 'MGLU3.SA', 'ITUB4.SA', 'GC=F', 'WEGE3.SA', 'ABEV3.SA', 'AERI3.SA', 'CIEL3.SA','PRIO3.SA', 'BBSE3.SA','HYPE3.SA','ASAI3.SA','SBSP3.SA','CPLE6.SA','ELET6.SA'

'''
ativo = 'ABEV3.SA'

''' 
2. BAIXAR DADOS DO ATIVO ESCOLHIDO
   O intervalo de datas deve começar após a data em que o ativo começou a ser negociado para evitar erros.
   
   Para exportar os dados para um arquivo externo:
   #dados_ativo.to_csv('dados_petroleo.csv')
'''

dados_ativo = yf.download(ativo)

'''
3. VERIFICAR CONSISTÊNCIA DOS DADOS
'''
dados_ativo['Adj Close'].plot()
plt.show()

'''
4. TRATAMENTO DE RETORNOS
'''
dados_ativo['retornos'] = dados_ativo['Adj Close'].pct_change().dropna()

'''
5. SEPARAR RETORNOS POSITIVOS E NEGATIVOS
'''
dados_ativo['retornos_positivos'] = dados_ativo['retornos'].apply(lambda x: x if x > 0 else 0)
dados_ativo['retornos_negativos'] = dados_ativo['retornos'].apply(lambda x: abs(x) if x < 0 else 0)
dados_ativo = dados_ativo.dropna()

'''
6. CÁLCULO DA MÉDIA DOS RETORNOS NOS ÚLTIMOS 22 DIAS
'''
dados_ativo['media_retornos_positivos'] = dados_ativo['retornos_positivos'].rolling(window=22).mean()
dados_ativo['media_retornos_negativos'] = dados_ativo['retornos_negativos'].rolling(window=22).mean()
dados_ativo = dados_ativo.dropna()

'''
7. CÁLCULO DO ÍNDICE DE FORÇA RELATIVA (RSI)
   RSI = 100 - 100 / (1 + média dos retornos positivos / média dos retornos negativos)
'''
dados_ativo['RSI'] = (100 - 100 / (1 + dados_ativo['media_retornos_positivos'] / dados_ativo['media_retornos_negativos']))

'''
8. SINALIZAÇÃO DE COMPRA E VENDA
   - Se RSI < 30, sinaliza 'compra'
   - Se RSI > 30, sinaliza 'venda'
'''
dados_ativo.loc[dados_ativo['RSI'] < 30, 'compra'] = 'sim'
dados_ativo.loc[dados_ativo['RSI'] > 30, 'compra'] = 'nao'

'''
8.1. MODELO SIMPLIFICADO DE COMPRA
   Identifica datas de compra com base no sinal 'sim'
'''
datas_compra = []

for i in range(len(dados_ativo)):
    if "sim" in dados_ativo['compra'].iloc[i]:
        datas_compra.append(dados_ativo.index[i + 1])

'''
8.1. MODELO AVANÇADO DE COMPRA E VENDA
   Identifica datas de compra e venda considerando o RSI nos próximos 10 dias
'''
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

'''
9. VISUALIZAÇÃO DOS DADOS DE COMPRA E VENDA
'''
'''
plt.figure(figsize=(12, 5))
plt.scatter(dados_ativo.loc[data_compra].index, dados_ativo.loc[data_compra]['Adj Close'], marker='^', c='g')
plt.plot(dados_ativo['Adj Close'], alpha=0.7)
plt.show()
'''

'''
10. CÁLCULO DOS LUCROS
'''
lucros = dados_ativo.loc[data_venda]['Open'].values / dados_ativo.loc[data_compra]['Open'].values - 1

'''
11. ANÁLISE DOS LUCROS
'''
operacoes_vencedoras = len(lucros[lucros > 0]) / len(lucros)
media_ganhos = np.mean(lucros[lucros > 0])
media_perdas = abs(np.mean(lucros[lucros < 0]))
expectativa_matematica_modelo = (operacoes_vencedoras * media_ganhos) - ((1 - operacoes_vencedoras) * media_perdas)
performance_acumulada = (np.cumprod((1 + lucros)) - 1)
retorno_buy_and_hold = dados_ativo['Adj Close'].iloc[-1] / dados_ativo['Adj Close'].iloc[0] - 1

# Exibir resultados
print(f"Operações Vencedoras: {operacoes_vencedoras}")
print(f"Média de Ganhos: {media_ganhos * 100:.2f}%")
print(f"Média de Perdas: {media_perdas * 100:.2f}%")
print(f"Expectativa Matemática do Modelo: {expectativa_matematica_modelo * 100:.2f}%")
print(f"Performance Acumulada: {performance_acumulada[-1] * 100:.2f}%")
print(f"Retorno Buy and Hold: {retorno_buy_and_hold * 100:.2f}%")


# Graficos Uteis


plt.figure(figsize = (12, 5))
plt.scatter(dados_ativo.loc[data_compra].index, dados_ativo.loc[data_compra]['Adj Close'], marker = '^', c = 'g')
plt.plot(dados_ativo['Adj Close'], alpha = 0.7)
plt.show()

'''
plt.figure(figsize = (12, 5))
plt.plot(data_compra, performance_acumulada)
plt.show()
'''
