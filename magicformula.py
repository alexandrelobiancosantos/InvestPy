import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados das empresas e filtrar por liquidez
dados_empresas = pd.read_csv("dados_empresas.csv")
dados_empresas = dados_empresas[dados_empresas['volume_negociado'] > 1000000]

# Calcular retornos mensais das empresas
dados_empresas['retorno'] = dados_empresas.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
dados_empresas['retorno'] = dados_empresas.groupby('ticker')['retorno'].shift(-1)

# Calcular ranking dos indicadores
dados_empresas['ranking_ev_ebit'] = dados_empresas.groupby('data')['ebit_ev'].rank(ascending=False)
dados_empresas['ranking_roic'] = dados_empresas.groupby('data')['roic'].rank(ascending=False)
dados_empresas['ranking_final'] = dados_empresas['ranking_ev_ebit'] + dados_empresas['ranking_roic']
dados_empresas['ranking_final'] = dados_empresas.groupby('data')['ranking_final'].rank()

# Filtrar empresas para criar as carteiras
dados_empresas = dados_empresas[dados_empresas['ranking_final'] <= 10]

# Calcular rentabilidade por carteira
rentabilidade_por_carteiras = dados_empresas.groupby('data')['retorno'].mean().to_frame()
rentabilidade_por_carteiras['modelo'] = (rentabilidade_por_carteiras['retorno'] + 1).cumprod() - 1
rentabilidade_por_carteiras = rentabilidade_por_carteiras.shift(1).dropna()

# Carregar dados do índice Bovespa (ibovespa) e calcular rentabilidade acumulada
ibov = pd.read_csv('ibov.csv')
retornos_ibov = ibov['fechamento'].pct_change().dropna()
retorno_acum_ibov = (1 + retornos_ibov).cumprod() - 1
rentabilidade_por_carteiras['ibovespa'] = retorno_acum_ibov.values
rentabilidade_por_carteiras = rentabilidade_por_carteiras.drop('retorno', axis=1)

# Configurar índice de datas
rentabilidade_por_carteiras.index = pd.to_datetime(rentabilidade_por_carteiras.index)

# Plotar gráficos de rentabilidade
plt.figure(figsize=(10, 6))
plt.plot(rentabilidade_por_carteiras.index, rentabilidade_por_carteiras['modelo'], label='Modelo')
plt.plot(rentabilidade_por_carteiras.index, rentabilidade_por_carteiras['ibovespa'], label='Ibovespa')
plt.xlabel('Data')
plt.ylabel('Rentabilidade Acumulada')
plt.title('Rentabilidade Acumulada do Modelo vs. Ibovespa')
plt.legend()
plt.show()

# Calcular e imprimir rentabilidade anualizada
rentabilidade_ao_ano = (1 + rentabilidade_por_carteiras.loc['2023-06-30', 'modelo']) ** (1/7.5) - 1
print(rentabilidade_ao_ano)
