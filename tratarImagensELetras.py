
from imagens_utils import tratarImagensAdaptativo
from imagens_utils import getLetrasAdaptativo

if __name__=='__main__':
    origem_imagens = 'amostra'
    destino_imagens = 'ajeitado'
    origem_letras = 'ajeitado'
    destino_letras = 'letras'
    
    tratarImagensAdaptativo(origem_imagens,destino_imagens)
    getLetrasAdaptativo(origem_letras,destino_letras)