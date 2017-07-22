# -*- coding: utf-8 -*-
from secrets import CONFIG
# ==============================================================================
# CONFIGURACIONES DE COLORES.
# ==============================================================================
HEADER = '\033[96m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
DARKBLUE = '\033[34m'

# ==============================================================================
# AWS LAMBDA.
# ==============================================================================
AWS_LAMBDA = {
    "AWS_ACCESS_KEY_ID": CONFIG.get('AWS_ACCESS_KEY_ID', None),
    "AWS_SECRET_ACCESS_KEY": CONFIG.get('AWS_SECRET_ACCESS_KEY', None)
}

AWS_REGIONS = {
    '0': {'region': 'us-east-1', 'name': 'Virginia'},
    '1': {'region': 'us-east-2', 'name': 'Ohio'},
    '2': {'region': 'us-west-1', 'name': 'California'},
    '3': {'region': 'us-west-2', 'name': 'Oregon'},
    '4': {'region': 'sa-east-1', 'name': 'Sao Paulo'},
    '5': {'region': 'ap-northeast-1', 'name': 'Tokio'},
    '6': {'region': 'eu-west-1', 'name': 'Irlanda'},
    '7': {'region': 'eu-west-2', 'name': 'Londres'},
    '8': {'region': 'eu-central-1', 'name': 'Alemania'}
}

# ==============================================================================
# EXCLUSION DE DIRECTORIOS
# ==============================================================================
BLACK_LIST_DIRECTORIES = [
    '.git',
    'templates'
]
