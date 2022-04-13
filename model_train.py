import cv2
import os
import numpy as np
import pickle
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense
from helpers import resize_to_fit

def getDados(pasta_imagens=None):
    dados = []
    rotulos = []
    imagens = paths.list_images(pasta_imagens)
    for arquivo in imagens:
        rotulo = arquivo.split(os.path.sep)[-2]
        imagem = cv2.imread(arquivo)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
        
        #PADRONIZAR TAMANHO IMAGEM 30x30
        imagem = resize_to_fit(imagem,30,30)
        
        #ADICIONAR DIMENSÃO 2
        imagem = np.expand_dims(imagem,axis=2)
        
        #ADICIONAR A DATA E LABEL
        rotulos.append(rotulo)
        dados.append(imagem)
    dados = np.array(dados,dtype="float")/255
    rotulos = np.array(rotulos)
    return dados,rotulos

dados,rotulos = getDados(pasta_imagens="base_letras")

(X_train, X_test, Y_train, Y_test) = train_test_split(dados, rotulos, test_size=0.25)

lb = LabelBinarizer().fit(Y_train)

Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)

# salvar o LabelBinarizer com pickle

with open('rotulos_modelo.dat','wb') as arquivo_pickle:
    pickle.dump(lb, arquivo_pickle)

modelo = Sequential()

# criar as camadas da rede neural
modelo.add(Conv2D(60,(5,5), padding="same", input_shape=(30,30,1), activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
# criar a 2ª camada
modelo.add(Conv2D(150,(5, 5), padding="same", activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
# # criar a 3ª camada
modelo.add(Conv2D(375, (5, 5), padding="same", activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
# # criar a 4ª camada
# modelo.add(Conv2D(625, (5, 5), padding="same", activation="relu"))
# modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
# mais uma camada
modelo.add(Flatten())
modelo.add(Dense(1024, activation="relu"))
# camada de saída
modelo.add(Dense(49, activation="softmax"))
# compilar todas as camadas

if __name__=='__main__':
    modelo.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    # treinar a rede neural
    modelo.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=49, epochs=30, verbose=1)
    # salvar o modelo
    modelo.save("modelo_treinado.hdf5")
