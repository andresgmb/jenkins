# -*- coding: utf-8 -*-
import re
from operator import truediv
import Levenshtein
import fuzzy


def aarnel_validation(data):
    """
    COEFICIENTE DE AARNEL EN VERSION GENERALIZADA PARA DOS STRINGS..
    Coeficiente de Aarnel es una mezcla de la distancia Levenshtein (LV) y
    Teoria de Metaphone (ME).
    Primero se calcula la distancia de los 2 string con LV, paralelamente se
    extraen las combinaciones foneticas con ME de los strings por individual y
    como resultado se obtienen 2 nuevos strings a los cuales tambien se le
    aplicara LV para compara su proximidad fonetica, posteriormente se les saca
    el promedio para obtener la media del cruce de proximidad literaria y
    proximidad fonetica.
    Parameters
    ----------
    address_1 : str
        String a comparar.
    address_2 : str
        String a comparar.
    Returns
    -------
    True:
        En caso del porcentaje obtenido sea mayor o igual al especificado por
        los administradores.
    False:
        En caso del porcentaje obtenido sea menor al especificado por los
        administradores
    :Authors:
        - Aarón Dominguez
        - Nel Perez
    Last Modification : 13.11.2017
    """
    pruebanadres4 = 0
    address_1 = data.get('address_1')
    address_2 = data.get('address_2')
    address_comparation = data.get('comparation_values')
    if address_1 is None or address_2 is None:
        return False
    try:
        digit = re.match('.+([0-9])[^0-9]*$', address_1)
        digit = digit.start(1)
        address_1 = address_1[:digit+1]
        address_1 = address_1.upper()
    except:
        pass
    try:
        digit = re.match('.+([0-9])[^0-9]*$', address_2)
        digit = digit.start(1)
        address_2 = address_2[:digit+1]
        address_2 = address_2.upper()
    except:
        pass
    cleaner = address_comparation
    if not cleaner:
        return False
    valid = truediv(address_comparation.get('percent_strength'), 100)
    cleaner_especials = address_comparation.get('special')
    cleaner_especials = cleaner_especials.split('|')
    for item in cleaner_especials:
        address_1 = address_1.replace(item, "")
        address_2 = address_2.replace(item, "")

    cleaner_words = address_comparation.get('word').upper()
    cleaner_words = cleaner_words.split('|')
    for item in cleaner_words:
        address_1 = address_1.replace(item + ' ', "")
        address_2 = address_2.replace(item + ' ', "")
    address_1 = address_1.replace(' ', "")
    address_2 = address_2.replace(' ', "")

    address_1 = address_1.replace(' ', "")
    address_2 = address_2.replace(' ', "")
    ratio_lev = Levenshtein.ratio(address_1, address_2)
    try:
        sound_first_dir = fuzzy.nysiis(address_1.upper())
        sound_second_dir = fuzzy.nysiis(address_2.upper())
        ratio_met = Levenshtein.ratio(sound_first_dir, sound_second_dir)
        media = (ratio_lev+ratio_met)/2
    except:
        media = 0
    if media >= valid:
        return True
    else:
        return False


def lambda_handler(event, context):
    data = {
        "address_1": event.get('address_1'),
        "address_2": event.get('address_2'),
        "comparation_values": {
            "percent_strength": event.get('percent_strength'),
            "word": event.get('word'),
            "special": event.get('special')
        }
    }
    aarnel = aarnel_validation(data)
    """
    Implementar funcion dispatcher hacia API.
    """
    return {'status': aarnel}