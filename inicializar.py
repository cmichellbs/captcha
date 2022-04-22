import os
import logging

logging.basicConfig(filename='inicializar.log', encoding='utf-8', level=logging.INFO)

try:
    os.system('pip3 install -r requirements.txt')
    logging.info('Instalado pacotes necessários')
except:
    logging.error('Erro ao instalar pacotes')
try:
    try:
        os.mkdir('ajeitado')
        logging.info('Pasta ajeitado criada com sucesso')
    except:
        logging.info('Pasta ajeitado já existe')
    try:
        os.mkdir('amostra')
        logging.info('Pasta amostra criada com sucesso')
    except:
        logging.info('Pasta amostra já existe')
    try:
        os.mkdir('base_letras')
        logging.info('Pasta base_letras criada com sucesso')
    except:
        logging.info('Pasta base_letras já existe')
    try:
        os.mkdir('bdcaptcha')
        logging.info('Pasta bdcaptcha criada com sucesso')
    except:
        logging.info('Pasta bdcaptcha já existe')
    try:
        os.mkdir('letras')
        logging.info('Pasta letras criada com sucesso')
    except:
        logging.info('Pasta letras já existe')
    try:
        os.mkdir('pis')
        logging.info('Pasta pis criada com sucesso')
    except:
        logging.info('Pasta pis já existe')
    try:
        os.mkdir('resolver')
        logging.info('Pasta resolver criada com sucesso')
    except:
        logging.info('Pasta resolver já existe')
    try:
        os.mkdir('tratado')
        logging.info('Pasta tratado criada com sucesso')
    except:
        logging.info('Pasta tratado já existe')
    logging.info('Pastas criadas com sucesso')
except:
    logging.info('Pastas já existem')
    