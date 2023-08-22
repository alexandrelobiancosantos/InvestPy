from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))


url = 'https://www.fundamentus.com.br/resultado.php'

driver.get(url)

local_tabela = '/html/body/div[1]/div[2]/table'

elemento = driver.find_element("xpath", local_tabela)

html_tabela = elemento.get_attribute('outerHTML')

tabela = pd.read_html(str(html_tabela), thousands = '.', decimal = ',')[0]
#print(tabela)
# Adiciona delay para testes do script
#time.sleep(5)

#set index p nome do ativo

tabela = tabela.set_index('Papel')
tabela = tabela[['Cotação', 'EV/EBIT', 'ROIC', 'Liq.2meses']]
#tabela.info()
tabela['ROIC'] = tabela['ROIC'].str.replace('%','')
tabela['ROIC'] = tabela['ROIC'].str.replace('.','')
tabela['ROIC'] = tabela['ROIC'].str.replace(',','.')
tabela['ROIC'] = tabela['ROIC'].astype(float)
#print(tabela)
#tabela.info()

tabela = tabela[tabela['Liq.2meses'] > 1000000]
#print(tabela)

tabela = tabela[tabela['EV/EBIT'] > 0]
tabela = tabela[tabela['ROIC'] > 0]
#print(tabela)

tabela['ranking_ev_ebit'] = tabela['EV/EBIT'].rank(ascending = True)
tabela['ranking_roic'] = tabela['ROIC'].rank(ascending = False)
tabela['ranking_final'] = tabela['ranking_ev_ebit'] + tabela['ranking_roic']

print(tabela)

tabela = tabela.sort_values('ranking_final')
print(tabela.head(10))