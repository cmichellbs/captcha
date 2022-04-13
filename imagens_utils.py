import base64
import glob
from random import randint
import os
import cv2
from PIL import Image

from geradorPis import geradorDePisPasep

from selenium import webdriver

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from helpers import resize_to_fit

def getImagens(xpath_refresh=None, xpath_imagem=None, pasta=None, auto_refresh=False, index=0):
    if auto_refresh:
        navegador.find_element_by_xpath(f'{xpath_refresh}').click()
    img = navegador.find_element_by_xpath(f'{xpath_imagem}').get_attribute('src').split(',')[1]
    img=base64.b64encode(base64.b64decode(img))
    fh = open(f"imagem{index}.png", "wb")
    fh.write(base64.decodebytes(img))
    fh.close()
    imagem = cv2.imread(f"imagem{index}.png",1)
    img_scale_up = cv2.resize(imagem, (0, 0), fx=3, fy=3)
    if pasta is not None:
        cv2.imwrite(f'{pasta}/imagem{index}.png',img_scale_up)
    cv2.imwrite(f'imagem{index}.png',img_scale_up)


def tratarImagensAdaptativo(origem = None,destino =None):
    arquivos = glob.glob(f'{origem}/*')
    for arquivo in arquivos:
        imagem = cv2.imread(arquivo,0)
        imagem = cv2.GaussianBlur(imagem,(5,7),5)
        #transformar em escala de cinza
        # imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
        # _, imagem_tratada = cv2.threshold(imagem_cinza,99,255, cv2.THRESH_TRUNC or cv2.THRESH_OTSU)
        imagem_tratada = cv2.adaptiveThreshold(imagem,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,661,138)
        nome_arquivo = os.path.basename(arquivo)
        cv2.imwrite(f'{destino}/{nome_arquivo}',imagem_tratada)
    # arquivos = glob.glob(f"{destino}/*")
    # for arquivo in arquivos:
    #     imagem = Image.open(arquivo)
    #     imagem = imagem.convert("P")
    #     imagem2 = Image.new("P",imagem.size,255)
    #     for x in range(imagem.size[1]):
    #         for y in range(imagem.size[0]):
    #             cor_pixel = imagem.getpixel((y,x))
    #             if cor_pixel < 127:
    #                 imagem2.putpixel((y,x),0)
    #     nome_arquivo = os.path.basename(arquivo)
    #     imagem2.save(f'{destino}/{nome_arquivo}')
        
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

