# Archivo de prueba.
import sys
sys.path.append('')

from aarnel_validation.aarnel_validation import aarnel_validation

# =============================================================================
# DATOS DE PRUEBA.
# =============================================================================

# Prueba para Aguas Andinas (formal_address y address [bills])
# Prueba efectiva (True), para prueba fallida, solo cambiar algunas de las
# direcciones: address_1 o address_2
data = {
    "address_1": u'Carabineros de Chile 22, 801, SANTIAGO, SANTIAGO (01/2014)',
    "address_2": u'CARABINEROS DE CHILE 22-801 ',
    "comparation_values": {
        "percent_strength": 50,
        "word": "AV|AVENIDA|BLOQUE|BLOCK|PJ|PJE|ENTREGAR|PASAJE|PA|"
        "CASA|DP|DPTO|DEPARTAMENTO|EDIF",
        "special": "!|@|#|$|/|.|-|\\u00b0"
    }
}

aarnel = aarnel_validation(data)

print(aarnel)