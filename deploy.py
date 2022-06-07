from datetime import datetime
import sys
import os
from selenium import webdriver
import base64
import re
from PIL import Image
import pandas as pd
from bs4 import BeautifulSoup as bs
import cv2
from selenium.webdriver.firefox.options import Options
from geradorPis import geradorDePisPasep
from random import randint
from quebrarCaptcha import quebrarCaptcha
import pandas as pd
import time
import logging

if sys.argv[1] == '-c':
    print('Excluindo arquivo de log da sessão anterior')
    os.system('rm -rf minerador.log')
else:
    print('Continuando o arquivo de log da sessão anterior')

logging.basicConfig(filename='minerador.log', encoding='utf-8', level=logging.INFO)



def get_imagem():
    img = navegador.find_element_by_xpath('//*[@id="img_captcha_serpro_gov_br"]').get_attribute('src').split(',')[1]
    img=base64.b64encode(base64.b64decode(img))
    fh = open(f"resolver/imagem.png", "wb")
    fh.write(base64.decodebytes(img))
    fh.close()
    imagem = cv2.imread("resolver/imagem.png",1)
    img_scale_up = cv2.resize(imagem, (0, 0), fx=3, fy=3)
    cv2.imwrite(f'resolver/imagem.png',img_scale_up)
    
    logging.info(f'{datetime.now()}:Imagem CAPTCHA capturada com sucesso')


dataset = pd.DataFrame()

option = Options()
option.headless = True
navegador = webdriver.Firefox(options=option,keep_alive=False)
navegador.get('http://rais.gov.br/sitio/consulta_trabalhador_identificacao.jsf')
for i in range(int(sys.argv[2])):
    pis = geradorDePisPasep()

    time.sleep(randint(1,4))

    src = navegador.page_source

    padrao_pis = '.id="j_idt[0-9]+:pis"'
    padrao_btn = '.name="j_idt[0-9]+:j_idt[0-9]+".value="Avançar"'



    input_pis = re.search(padrao_pis, src)
    input_pis = input_pis.group().split('="')[1].split('"')[0]
    btn_avancar = re.search(padrao_btn,src)
    btn_avancar = btn_avancar.group().split('="')[1].split('"')[0]

    navegador.find_element_by_name(input_pis).send_keys(f'{pis}')

    navegador.find_element_by_id('btnRecarregar_captcha_serpro_gov_br').click()

    time.sleep(randint(1,4))

    
    tentativaPis = True
    while tentativaPis:
        try:
            get_imagem()
            time.sleep(randint(1,4))
            captcha = quebrarCaptcha()
            navegador.find_element_by_xpath('//*[@id="txtTexto_captcha_serpro_gov_br"]').send_keys(f'{captcha}')
            navegador.find_element_by_name(btn_avancar).click()
            try:
                continuar = navegador.find_element_by_xpath('/html/body/div[2]/div[5]/ul/li').get_attribute('innerHTML')
                continuar = continuar.strip()
            except:
                continuar = None
            
            if continuar == None:
                logging.info(f'{datetime.now()}:{pis} encontrado!')
                trabalhador = navegador.page_source
                df_pis = pd.read_html(trabalhador)
                df_pis = df_pis[0]
                df_pis['pis'] = pis
                nome = navegador.find_element_by_xpath('//*[@id="j_idt27"]/div[2]/div/p').get_attribute('innerHTML').split('-')[1].strip()
                df_pis['nome'] = nome
                dataset = dataset.append(df_pis,ignore_index=True)
                src2 = navegador.page_source
                padrao_voltar = '.name="j_idt[0-9]+:j_idt[0-9]+".value="Voltar"'
                btn_voltar = re.findall(padrao_voltar,src2)
                btn_voltar = btn_voltar[0].split('="')[1].split('"')[0]
                navegador.find_element_by_name(btn_voltar).click()
                tentativaPis = False
            elif continuar == 'PIS inválido.':
                logging.info(f'{datetime.now()}:{pis} inválido!')
                tentativaPis = False
                time.sleep(randint(1,4))
            elif continuar == 'Por favor, repita os caracteres da imagem.':
                logging.info(f'{datetime.now()}:Repetindo captcha para {pis}')
                navegador.find_element_by_id('btnRecarregar_captcha_serpro_gov_br').click()
                tentativaPis = True
                time.sleep(randint(1,4))
            else:
                tentativaPis = False
                logging.info(f'{datetime.now()}:{pis} não existe na base RAIS')
        except:
            tentativaPis = False
            logging.error(f"{datetime.now()}:Erro ao tentar resolver o captcha para os pis {pis}.")

dataset.to_csv('base_pis.csv',index=False)
navegador.close()
navegador.quit()
logging.info(f'{datetime.now()}:Fim')
print(sys.argv[2] + ' PISs verificados')

