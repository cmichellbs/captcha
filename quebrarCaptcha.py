from datetime import datetime
import logging
from cv2 import sort
from keras.models import load_model
from helpers import resize_to_fit
import numpy as np
import cv2
import pickle
from imagens_utils import tratarImagensAdaptativo
from imagens_utils import getLetrasAdaptativo
import os
import glob

def quebrarCaptcha ():
    with open("rotulos_modelo.dat", "rb") as arquivo_tradutor:
        lb = pickle.load(arquivo_tradutor)

    modelo = load_model("modelo_treinado.hdf5")
    tratarImagensAdaptativo('resolver', 'tratado')
    getLetrasAdaptativo('tratado','letras')
    captcha = []
    letras = glob.glob('letras/*')
    letras.sort()
    for letra in letras:
        img = cv2.imread(letra)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img=resize_to_fit(img,30,30)
        img = np.expand_dims(img, axis=2)
        img = np.expand_dims(img, axis=0)
        predict = modelo.predict(img)
        predict= lb.inverse_transform(predict)[0]
        captcha.append(predict)
    texto_previsao = "".join(captcha)
    print(texto_previsao)
    os.system('rm -rf resolver/*')
    os.system('rm -rf tratado/*')
    os.system('rm -rf letras/*')
    logging.info(f'{datetime.now()}:Captcha resolvido!')
    return texto_previsao
if __name__=='__main__':
    quebrarCaptcha()

    
