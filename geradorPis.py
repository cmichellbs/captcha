import string
from random import randint
import pandas as pd

def geradorDePisPasep( formatar=False ):

   # 9 números aleatórios
   arNumeros = []
   for i in range(10):
      arNumeros.append( randint(0,9) )      

   # Calculado DV
   somaJ = ( arNumeros[0] * 3 ) + ( arNumeros[1] * 2 ) + ( arNumeros[2] * 9 ) + ( arNumeros[3] * 8 )  + ( arNumeros[4] * 7 ) + ( arNumeros[5] * 6 ) + ( arNumeros[6] * 5 )  + ( arNumeros[7] * 4 ) + ( arNumeros[8] * 3 ) + ( arNumeros[9] * 2 )

   restoJ = somaJ % 11
   subtracao = 11 - restoJ

   if ( subtracao == 10 or subtracao == 11 ):
      j = 0
   else:
      j = subtracao   

   arNumeros.append( j )

   pis = ''.join(str(x) for x in arNumeros)

   if formatar:
      return pis[ :10 ] + '-' + pis[ 10: ]
   else:
      return pis


if __name__ == '__main__':
   pis = []
   for i in range(500000):
      pis.append( geradorDePisPasep())
   df = pd.DataFrame( pis, columns=['pis'] )
   df.drop_duplicates(subset='pis', keep='first')
   df.to_csv( 'pis/pis.csv', index=False )