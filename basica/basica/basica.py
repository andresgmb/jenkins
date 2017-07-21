# -*- coding: utf-8 -*-

# 20 de Julio - x21

######################
## Archivo - Basica ##
######################

import Levenshtein
import fuzzy

def basica(numero):
    suma = 0
    for x in range(0, numero):
        suma += x
    return suma