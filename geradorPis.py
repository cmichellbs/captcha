import string
from random import randint
import pandas as pd

def geradorDePisPasep( formatar=False ):

   # 9 números aleatórios
   arNumeros = []
   arNumeros.append(randint(1,2))
   for i in range(9):
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
