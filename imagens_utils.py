import logging


import base64
import glob
from random import randint
import os
import cv2
from PIL import Image
from datetime import datetime


from helpers import resize_to_fit


def tratarImagensAdaptativo(origem = None,destino =None):
    arquivos = glob.glob(f'{origem}/*')
    for arquivo in arquivos:
        imagem = cv2.imread(arquivo,0)
        imagem = cv2.GaussianBlur(imagem,(5,7),5)
        
        imagem_tratada = cv2.adaptiveThreshold(imagem,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,661,138)
        nome_arquivo = os.path.basename(arquivo)
        cv2.imwrite(f'{destino}/{nome_arquivo}',imagem_tratada)
    logging.info(f'{datetime.now()}:Tratamento de imagens realizado com sucesso')
    
        
def getLetrasAdaptativo(origem= None,destino=None):
    arquivos = glob.glob(f'{origem}/*')
    for imagem in arquivos:
        img = cv2.imread(imagem)
        height = img.shape[0]
        width = img.shape[1]
        width_cutoff = width // 6
        left1 = img[:, :width_cutoff]
        right1 = img[:, width_cutoff:]
        letras = []
        letras.append(img[:, :width_cutoff+20])
        letras.append(img[:, width_cutoff+20:2*width_cutoff+12])
        letras.append(img[:, 2*width_cutoff+12:3*width_cutoff+12])
        letras.append(img[:, 3*width_cutoff+12:4*width_cutoff+12])
        letras.append(img[:, 4*width_cutoff+12:5*width_cutoff+12])
        letras.append(img[:, 5*width_cutoff+12:])
        i=0
        for letra in letras:
            i+=1
            nome_arquivo = os.path.basename(imagem).replace(".png",f"letra{i}.png")
            cv2.imwrite(f'{destino}/{nome_arquivo}',letra)
    logging.info(f'{datetime.now()}:Letras extraídas das imagens sucesso')

def getLetras(origem= None):
    arquivos = glob.glob(f'{origem}/*')
    for imagem in arquivos:
        img = cv2.imread(imagem)
        height = img.shape[0]
        width = img.shape[1]
        width_cutoff = width // 6
        left1 = img[:, :width_cutoff]
        right1 = img[:, width_cutoff:]
        letras = []
        letras.append(img[:, :width_cutoff+20])
        letras.append(img[:, width_cutoff+20:2*width_cutoff+12])
        letras.append(img[:, 2*width_cutoff+12:3*width_cutoff+12])
        letras.append(img[:, 3*width_cutoff+12:4*width_cutoff+12])
        letras.append(img[:, 4*width_cutoff+12:5*width_cutoff+12])
        letras.append(img[:, 5*width_cutoff+12:])
    return letras

