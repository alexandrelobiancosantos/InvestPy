from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time



'''

'''

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

driver.get('https://www.fundamentus.com.br/resultado.php')

local_tabela = '/html/body/div[1]/div[2]/table'
#print(local_tabela)
tabela = driver.find_element('xpath', local_tabela)
#print(tabela)
html_tabela = tabela.get_attribute('outerHTML')
#print(html_tabela)
tabela = pd.read_html(str(html_tabela), thousands='.', decimal=',')
print(tabela)
# Adiciona delay para testes do script
#time.sleep(5)

