from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, JavascriptException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from datetime import datetime
import subprocess
import pandas as pd
import openpyxl as workbook
import numpy
import os
import sys
import time
import re

# Atualiza versão do Webdriver


servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

# Definição do tempo limite de espera implícito

navegador.implicitly_wait(30)

# Acessando o site e maximizando a janela

navegador.get("https://negocios.santander.com.br/RcbWeb/")
navegador.maximize_window()
###time.sleep(3)

# Encontre os elementos de entrada (input) e preencha-os

navegador.find_element(By.XPATH, '//*[@id="j_id_x:__13_2"]').send_keys('03.689.477/0001-14')
time.sleep(1)
navegador.find_element(By.XPATH, '//*[@id="j_id_x:__16"]').send_keys("dnr.ad")
time.sleep(1)
navegador.find_element(By.XPATH, '//*[@id="j_id_x:__18"]').send_keys("Loki@198")

time.sleep(10)


# Feche o navegador
navegador.quit()
