import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Configuração para suprimir advertências de atribuição encadeada
pd.options.mode.chained_assignment = None

'''
1. ESCOLHER A LISTA DE ATIVOS
   Pesquise nomes de ativos em https://finance.yahoo.com/
'''
#ativos = ['PETR4.SA', 'VALE', 'AMER3.SA', 'MGLU3.SA', 'ITUB4.SA', 'BRKM5.SA', 'VALE3.SA', 'ITUB4.SA', 'BRVALE']
ativos = ['PETR4.SA', 'PETR3.SA', 'VALE3.SA', 'MGLU3.SA', 'ITUB4.SA', 'BRKM5.SA', 'GC=F', 'WEGE3.SA', 'ABEV3.SA', 'AERI3.SA', 'CIEL3.SA','PRIO3.SA', 'BBSE3.SA','HYPE3.SA','ASAI3.SA','SBSP3.SA','CPLE6.SA','ELET6.SA']

# Dicionário para armazenar os resultados de cada ativo
resultados_por_ativo = {}

# Iterar sobre a lista de ativos
for ativo in ativos:

    # Baixar dados do ativo escolhido
    # Perido definido
    # dados_ativo = yf.download(ativo, '2020-12-31', '2023-08-14')
    # Perido desde 2020
    dados_ativo = yf.download(ativo, '2013-12-31')

    # Calcular os retornos diários
    dados_ativo['retornos'] = dados_ativo['Adj Close'].pct_change().dropna()

    # Separar retornos positivos e negativos
    dados_ativo['retornos_positivos'] = dados_ativo['retornos'].apply(lambda x: x if x > 0 else 0)
    dados_ativo['retornos_negativos'] = dados_ativo['retornos'].apply(lambda x: abs(x) if x < 0 else 0)
    dados_ativo = dados_ativo.dropna()

    # Calcular médias dos retornos nos últimos 22 dias
    dados_ativo['media_retornos_positivos'] = dados_ativo['retornos_positivos'].rolling(window=22).mean()
    dados_ativo['media_retornos_negativos'] = dados_ativo['retornos_negativos'].rolling(window=22).mean()
    dados_ativo = dados_ativo.dropna()

    # Calcular o RSI
    dados_ativo['RSI'] = (100 - 100 / (1 + dados_ativo['media_retornos_positivos'] / dados_ativo['media_retornos_negativos']))

    # Identificar sinais de compra e venda
    dados_ativo.loc[dados_ativo['RSI'] < 30, 'compra'] = 'sim'
    dados_ativo.loc[dados_ativo['RSI'] > 30, 'compra'] = 'nao'

    # Identificar datas de compra
    datas_compra = []
    for i in range(len(dados_ativo)):
        if "sim" in dados_ativo['compra'].iloc[i]:
            datas_compra.append(dados_ativo.index[i + 1])

    # Identificar datas de venda
    datas_venda = []
    for i in range(len(dados_ativo)):
        if "sim" in dados_ativo['compra'].iloc[i]:
            data_compra = dados_ativo.index[i + 1]
            for j in range(1, 11):
                if dados_ativo['RSI'].iloc[i + j] > 40:
                    datas_venda.append(dados_ativo.index[i + j + 1])
                    break
                elif j == 10:
                    datas_venda.append(dados_ativo.index[i + j + 1])

    # Calcular os lucros
    lucros = dados_ativo.loc[datas_venda]['Open'].values / dados_ativo.loc[datas_compra]['Open'].values - 1

    # Calcular estatísticas
    operacoes_vencedoras = len(lucros[lucros > 0]) / len(lucros)
    media_ganhos = np.mean(lucros[lucros > 0])
    media_perdas = abs(np.mean(lucros[lucros < 0]))
    expectativa_matematica_modelo = (operacoes_vencedoras * media_ganhos) - ((1 - operacoes_vencedoras) * media_perdas)
    performance_acumulada = (np.cumprod((1 + lucros)) - 1)
    retorno_buy_and_hold = dados_ativo['Adj Close'].iloc[-1] / dados_ativo['Adj Close'].iloc[0] - 1

    # Armazenar resultados no dicionário
    resultados_por_ativo[ativo] = {
        'Operações Vencedoras': operacoes_vencedoras,
        'Média de Ganhos': media_ganhos * 100,
        'Média de Perdas': media_perdas * 100,
        'Expectativa Matemática do Modelo': expectativa_matematica_modelo * 100,
        'Performance Acumulada': performance_acumulada[-1] * 100,
        'Retorno Buy and Hold': retorno_buy_and_hold * 100
    }
'''
# Exibir resultados para cada ativo
for ativo, resultados in resultados_por_ativo.items():
    print(f"Resultados para o ativo: {ativo}")
    for metrica, valor in resultados.items():
        print(f"{metrica}: {valor:.2f}")
    print("=" * 40)'''

# Exibir resultados em forma de tabela
print("Resultados por Ativo:")
print("=" * 85)
print("{:<10} {:<20} {:<20} {:<25} {:<25} {:<25} {:<25}".format(
    "Ativo", "Operações Vencedoras", "Média de Ganhos (%)", "Média de Perdas (%)",
    "Expectativa Matemática (%)", "Performance Acumulada (%)", "Retorno Buy and Hold (%)"))
print("=" * 85)

for ativo, resultados in resultados_por_ativo.items():
    print("{:<10} {:<20.2f} {:<20.2f} {:<25.2f} {:<25.2f} {:<25.2f} {:<25.2f}".format(
        ativo,
        resultados['Operações Vencedoras'],
        resultados['Média de Ganhos'],
        resultados['Média de Perdas'],
        resultados['Expectativa Matemática do Modelo'],
        resultados['Performance Acumulada'],
        resultados['Retorno Buy and Hold']
    ))
    
