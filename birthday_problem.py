# Description: Script to apply the birthday paradox to collision probabilities 
#              in hash functions.
# Phase: Theorical study
# Author: Luis Palazón Simón

import math
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times"],
    "font.sans-serif": ["Computer Modern Sans serif"],
    "font.monospace": ["Computer Modern Typewriter"],
    "axes.labelsize": 28,
    "font.size": 28,
    "legend.fontsize": 24,
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
    "figure.figsize": (14, 10)
})

# ---------------------------------------------------------------
# HASH FUNCTIONS WITH FIXED LENGTH DIGESTS
# ---------------------------------------------------------------

def numPossibleDigests(alphabet_length, digest_length):
  '''
  Returns the number of possible digests for a hash function
  '''
  return alphabet_length ** digest_length

# both hexadecimal -> A = {0,1,...,9,a,b,...,f}
numPossibleDigest_TLSH = numPossibleDigests(alphabet_length=16, digest_length=70)
print("El número de resúmenes posibles de TLSH es", numPossibleDigest_TLSH)
# and binary -> A = {0,1}, l = 35B * 8bits/B
# print("El número de resúmenes posibles de TLSH es", numPossibleDigests(alphabet_length=2, digest_length=35*8))

numPossibleDigest_Nilsimsa = numPossibleDigests(alphabet_length=16, digest_length=64)
print("El número de resúmenes posibles de Nilsimsa es", numPossibleDigest_Nilsimsa)
# numPossibleDigest_Nilsimsa = numPossibleDigests(alphabet_length=2, digest_length=32*8)
# print("El número de resúmenes posibles de Nilsimsa es", numPossibleDigest_Nilsimsa)

def birthdayProblem(n, d=365):
  '''
  Returns the probability of a birthday collision in a group of n people
  '''
  return 1 - math.factorial(d) / (d**n * math.factorial(d-n))

# print(birthdayProblem(23)) # factorial() argument should not exceed 9223372036854775807

def probAprox(n,d):
  '''
  Returns the approximate probability of a collision in a group of n people in a year of d days
  '''
  return 1 - math.exp(-n*(n-1)/(2*d))

def probAproxx(n,d):
  '''
  Returns the approximate probability of a collision in a group of n people in a year of d days
  '''
  return 1 - math.exp(-n**2/(2*d))

print("La probabilidad de colisión con la primera aproximación en TLSH es",  probAprox(10**35, numPossibleDigest_TLSH))
print("La probabilidad de colisión con la segunda aproximación en TLSH es",  probAproxx(10**35, numPossibleDigest_TLSH))

def numMuestrasNecesarias(p, d):
  '''
  El numero de muestras necesarias para alcanzar una probabilidad
  aproximada de colision p en un espacio de d elementos.
  '''
  return math.sqrt(-2 * d * math.log(1-p))

numMuestrasNecesarias(0.5, numPossibleDigest_TLSH)
print("El número de muestras necesarias para alcanzar la probabilidad de colisión del 0.5 en TLSH es", numMuestrasNecesarias(0.5, numPossibleDigest_TLSH))

# GRAPH TLSH
pValues = np.arange(0.0000000000000001, 1, 0.0000001)
nValues = [numMuestrasNecesarias(p, numPossibleDigest_TLSH) for p in pValues]
plt.plot(nValues, pValues)
plt.title(r'Probabilidad de colisión en función del número de muestras en \texttt{TLSH}')
plt.xlabel('Número de muestras')
plt.ylabel('Probabilidad de colisión')
# plt.legend()
plt.grid(True)
# Ajustar el grid
# max_x = max(nValues)
# plt.xticks(np.linspace(0, max_x, 10))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.show()

# GRAPH NILSIMSA
pValues = np.arange(0.0000000000000001, 1, 0.0000001)
nValues = [numMuestrasNecesarias(p, numPossibleDigest_Nilsimsa) for p in pValues]
plt.plot(nValues, pValues)
plt.title('Probabilidad de colisión en función del número de muestras en Nilsimsa')
plt.xlabel('Número de muestras')
plt.ylabel('Probabilidad de colisión')
# plt.legend()
plt.grid(True)
# Ajustar el grid
# max_x = max(nValues)
# plt.xticks(np.linspace(0, max_x, 10))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.show()

# ---------------------------------------------------------------
# HASH FUNCTIONS WITH VARIABLE LENGTH DIGESTS
# ---------------------------------------------------------------

def numPossibleDigestsV(alphabet_length, max_digest_length):
  ''' Assume that the minimum length of the hash is 1
      and that the maximum length is max_digest_length '''
  sum = 0
  for digest_length in range(max_digest_length, 0, -1): # [max_digest_length, max_digest_length-1, ..., 1]
    sum += alphabet_length ** digest_length
  return sum

"""
numPossibleDigestsVariable $= \sum_{n=1}^{max\_len} a^n$ siendo $a=\vert$Alfabeto$\vert$

## SSDEEP
Length of an individual fuzzy hash signature component:

SPAMSUM_LENGTH = 64

The longest possible length for a fuzzy hash signature (without the filename) is:

FUZZY_MAX_RESULT = 2 * SPAMSUM_LENGTH + 20 = 2 * 64 + 20 = 148 ASCII characters / bytes

FUZZY_MAX_RESULT - 1 = 147 # Exclude terminating '\0'
"""

# SSDEEP
alphabet_length = 26 * 2 + 10 + 3 # mayusc, minusc, cifras y :+/
max_digest_length = 147
numPossibleDigest_ssdeep = numPossibleDigestsV(alphabet_length, max_digest_length)
print("ssdeep |H| =", numPossibleDigest_ssdeep)

# GRAPH SSDEEP
pValues = np.arange(0.0000000000000001, 1, 0.0000001)
nValues = [numMuestrasNecesarias(p, numPossibleDigest_ssdeep) for p in pValues]
plt.plot(nValues, pValues)
plt.title(r'Probabilidad de colisión en función del número de muestras en \texttt{SSDEEP}')
plt.xlabel('Número de muestras')
plt.ylabel('Probabilidad de colisión')
# plt.legend()
plt.grid(True)
# Ajustar el grid
# max_x = max(nValues)
# plt.xticks(np.linspace(0, max_x, 10))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.show()