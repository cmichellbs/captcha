from cv2 import sort
from keras.models import load_model
from helpers import resize_to_fit
import numpy as np
import cv2
import pickle
from imagens_utils import tratarImagensAdaptativo
from imagens_utils import getLetrasAdaptativo
from quebrarCaptcha import quebrarCaptcha
import os
from imutils import paths


def organizarImagens(origem = None):
    with open("rotulos_modelo.dat", "rb") as arquivo_tradutor:
        lb = pickle.load(arquivo_tradutor)

    imagens = paths.list_images(origem)
    modelo =load_model("modelo_treinado.hdf5")
    for arquivo in imagens:
        img = cv2.imread(arquivo)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img=resize_to_fit(img,30,30)
        img = np.expand_dims(img, axis=2)
        img = np.expand_dims(img, axis=0)
        letra = modelo.predict(img)
        letra= lb.inverse_transform(letra)[0]
        os.system(f'mv {arquivo} /home/christhian.souza/projects/captcha/base_letras/{letra}')


if __name__=='__main__':
    origem = 'letras'
    organizarImagens(origem)