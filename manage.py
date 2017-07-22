# -*- coding: utf-8 -*-
import re
import sys
import json
from os import path
from os import walk
from os import system
from os import rename
from os import listdir
from os import makedirs
from shutil import copy
from shutil import copytree
from string import Template
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import traceback

# HERRAMIENTAS EXTERNAS..
import boto3
from tabulate import tabulate

# ==============================================================================
# CONFIGURACIONES DE COLORES.
# ==============================================================================
from settings import HEADER
from settings import OKBLUE
from settings import OKGREEN
from settings import WARNING
from settings import FAIL
from settings import END
from settings import BOLD
from settings import UNDERLINE
from settings import DARKBLUE

# ==============================================================================
# AWS LAMBDA
# ==============================================================================
from settings import AWS_LAMBDA
from settings import AWS_REGIONS

# ==============================================================================
# OTRAS CONFIGURACIONES
# ==============================================================================
from settings import BLACK_LIST_DIRECTORIES

__version__ = '0.4.0'


def header(text):
    u"""
    Imprime el un header.
    """
    system("clear")
    print HEADER + "==========================================" + END
    print HEADER + text + END
    print HEADER + "==========================================" + END


# ==============================================================================
# FUNCIONES PARA EL PROCESO DE CREACION
# ==============================================================================
def python_creator(params):
    u"""
    """
    create_requirements(params.get('project', None))
    create_secrets(params.get('project', None))
    create_makefile(params)
    create_readme(params)
    create_changelog(params)
    create_function(params)


def nodejs_creator(params):
    u"""
    """
    create_modules(params)
    create_secrets(params.get('project', None))
    create_makefile(params)
    create_readme(params)
    create_changelog(params)
    create_function(params)


AVALILABLE_ENVIRONMENTS = {
    'python': {
        'function': python_creator,
        'extension': 'py'
    },
    'nodejs': {
        'function': nodejs_creator,
        'extension': 'js'
    }
}


def create_lambda_function(args):
    u"""
    Crea una función lambda con toda su estructura de archivos base.
    """
    header("CREACIÓN DE FUNCIÓN LAMBDA")
    params = {}
    available_environment = []
    available_environments = {}
    for idx, i in enumerate(next(walk('./templates'))[1]):
        available_environments[str(idx)] = i
        available_environment.append([
            idx,
            i
        ])
    table = tabulate(
        available_environment,
        headers=['ID', 'AMBIENTE'],
        tablefmt='orgtbl'
    )
    print table
    print ""
    option = raw_input(
        ''.join((BOLD, "Selecionar ID de ambiente de desarrollo: ", END))
    )
    if available_environments.get(option, {}):
        params['environment'] = available_environments.get(option, {})
        params['runtime_version'] = raw_input(
            ''.join((BOLD, "Runtime version: ", END))
        )
        # params['project'] = raw_input(
        #     ''.join((BOLD, "Nombre del proyecto: ", END))
        # )
        params['function_name'] = raw_input(
            ''.join((BOLD, "Nombre de la función lambda: ", END))
        )
        params['project'] = params['function_name']
        params['description'] = raw_input(
            ''.join((BOLD, "Descripción de la función lambda: ", END))
        )

        aws_regions = []
        for idx, i in enumerate(AWS_REGIONS.keys()):
            aws_regions.append([
                i,
                AWS_REGIONS[i].get('region', ''),
                AWS_REGIONS[i].get('name', '')
            ])
        aws_regions = sorted(
            aws_regions,
            key=lambda k: k[0]
        )
        print ''
        print DARKBLUE, "     REGIONES DISPONIBLES", END
        print ''
        table = tabulate(
            aws_regions,
            headers=[
                ''.join((BOLD, 'ID', END)),
                ''.join((BOLD, 'REGION', END)),
                ''.join((BOLD, 'NOMBRE', END))
            ],
            tablefmt='orgtbl'
        )
        print table
        print ''
        print ''.join((BOLD, "Indicar ID de la región aws para deployment", END))
        option = raw_input(''.join((
            WARNING, "DEFECTO [us-west-2]: ", END
        )))
        params['aws_region'] = AWS_REGIONS.get(option, {}).get('region', 'us-west-2')
        if create_directories(params.get('project', None)):
            AVALILABLE_ENVIRONMENTS.get(params.get('environment', {})).get('function')(params)
            # create_requirements(params.get('project', None))
            # create_secrets(params.get('project', None))
            # create_makefile(params)
            # create_readme(params)
            # create_changelog(params)
            # create_function(params)
        else:
            print ''.join((
                WARNING,
                "[WARNING] El nomnbre del proyecto lambda ya existe."
            ))
    else:
        print ''.join((
            FAIL,
            "[ERROR] Ambiente no disponible."
        ))


def create_directories(project):
    u"""
    Crea el árbol de directorios.
    """
    if not path.exists(project):
        header("PROYECTO '%s'" % (project))
        makedirs('/'.join(('.', project, project)))
        print ''.join((OKGREEN, "[OK] Directorio de proyecto", END))
        return True
    return False


def create_requirements(project):
    u"""
    Crea el archivo secrets.json.
    """
    try:
        open(
            '/'.join(('.', project, "requirements")),
            'a'
        ).close()
        print ''.join((OKGREEN, "[OK] requirements", END))
    except:
        print ''.join((
            FAIL,
            "[ERROR] No fue posible crear el archivo requirements."
        ))


def create_secrets(project):
    u"""
    Crea el archivo secrets.json.
    """
    try:
        file_content = open("./templates/secrets", "r")
        secrets = open('/'.join(('.', project, "secrets.json")), "w")
        secrets.write(file_content.read())
        secrets.close()
        print ''.join((OKGREEN, "[OK] secrets.json", END))
    except:
        print ''.join((
            FAIL,
            "[ERROR] No fue posible crear el archivo secrets.json"
        ))


def create_makefile(params):
    u"""
    Crea el archivo Makefile.
    """
    try:
        file_content = open(
            "".join((
                "./templates/",
                params['environment'],
                "/makefile")),
            "r"
        )
        makefile = open('/'.join(('.', params.get('project'), "Makefile")), "w")
        file_template = Template(file_content.read())
        file_content = file_template.safe_substitute(params)
        makefile.write(file_content)
        makefile.close()
        print ''.join((OKGREEN, "[OK] Makefile", END))
    except:
        print ''.join((
            FAIL,
            "[ERROR] No fue posible crear el archivo Makefile"
        ))


def create_readme(params):
    u"""
    Crea el archivo README.rst.
    """
    try:
        file_content = open("./templates/readme", "r")
        makefile = open(
            '/'.join((
                '.',
                params.get('project'),
                "README.rst"
            )),
            "w"
        )
        file_template = Template(file_content.read())
        file_content = file_template.safe_substitute(params)
        makefile.write(file_content)
        makefile.close()
        print ''.join((OKGREEN, "[OK] README.rst", END))
    except:
        print ''.join((
            FAIL,
            "[ERROR] No fue posible crear el archivo README"
        ))


def create_changelog(params):
    u"""
    Crea el archivo CHANGELOG.md.
    """
    try:
        file_content = open("./templates/changelog", "r")
        makefile = open(
            '/'.join((
                '.',
                params.get('project'),
                "CHANGELOG.md"
            )),
            "w"
        )
        file_template = Template(file_content.read())
        file_content = file_template.safe_substitute(params)
        makefile.write(file_content)
        makefile.close()
        print ''.join((OKGREEN, "[OK] CHANGELOG", END))
    except:
        print ''.join((
            FAIL,
            "[ERROR] No fue posible crear el archivo CHANGELOG"
        ))


def create_function(params):
    u"""
    Crea el archivo de la función principal.
    """
    try:
        file_content = open(
            "".join((
                "./templates/",
                params['environment'],
                "/function")),
            "r"
        )
        function_file = open(
            ''.join((
                './',
                params.get('project'), '/',
                params.get('project'), '/',
                params.get('function_name'),
                '.',
                AVALILABLE_ENVIRONMENTS.get(params.get('environment', {})).get('extension')
            )),
            "w"
        )
        file_template = Template(file_content.read())
        file_content = file_template.safe_substitute(params)
        function_file.write(file_content)
        function_file.close()
        print ''.join((OKGREEN, "[OK] Función exitosa", END))
    except:
        print ''.join((
            FAIL,
            "[ERROR] No fue posible crear el archivo de la función principal"
        ))
        print traceback.format_exc()


def create_modules(params):
    u"""
    """
    try:
        project = params.get('project', None)
        if path.exists(project):
            makedirs('/'.join(('.', project, project, 'modules')))
            print ''.join((OKGREEN, "[OK] Directorio de modulos", END))
            return True
        return False
    except:
        print ''.join((
            FAIL,
            "[ERROR] No fue posible crear el directorio de módulos."
        ))
        print traceback.format_exc()


# ==============================================================================
# LISTADO DE FUNCIONES
# ==============================================================================
def list_lambda_function(args):
    u"""
    Enlista los proyectos lambda existentes en localhost.
    """
    header("LISTADO DE PROYECTOS LAMBDAS")
    projects_dictionary = {}
    projects_summary = []
    projects_aws_lambda = []
    projects_regions = {}
    print ''.join((WARNING, 'Recolectando funciones lambda', END))
    print ''.join((WARNING, "------------------------------------------", END))
    for i in AWS_REGIONS.values():
        print ''.join((WARNING, 'Consultando region: ', i.get('region'), END)),
        try:
            client = boto3.client(
                'lambda',
                region_name=i.get('region'),
                aws_access_key_id=AWS_LAMBDA.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=AWS_LAMBDA.get('AWS_SECRET_ACCESS_KEY')
            )
            response = client.list_functions()
            for function in response.get('Functions'):
                projects_aws_lambda.append(function.get('FunctionName'))
                if projects_regions.get(function.get('FunctionName'), None):
                    projects_regions[function.get('FunctionName')].append(i.get('region'))
                else:
                    projects_regions[function.get('FunctionName')] = [i.get('region')]
            print ''.join((OKGREEN, '[OK]', END))
        except:
            print ''.join((FAIL, '[ERROR]', END))
            # print traceback.format_exc()

    print ''.join((WARNING, "------------------------------------------", END))
    print ''
    lambda_projects = []
    tmp_lambda_projects = next(walk('.'))[1]
    for i in tmp_lambda_projects:
        if i not in BLACK_LIST_DIRECTORIES:
            lambda_projects.append(i)
    for idx, i in enumerate(lambda_projects):
        if 'test' in i:
            if i in projects_aws_lambda:
                projects_summary.append([
                    ''.join((BOLD, DARKBLUE, str(idx), END)),
                    ''.join((BOLD, DARKBLUE, i, END)),
                    ''.join((BOLD, DARKBLUE, 'Test', END)),
                    ''.join((BOLD, DARKBLUE, ' '.join(projects_regions[i]), END)),
                ])
                projects_dictionary[idx] = {
                    'region': projects_regions[i],
                    'function_name': i
                }
                projects_regions.pop(i)
            else:
                projects_summary.append([
                    ''.join((BOLD, DARKBLUE, str(idx), END)),
                    ''.join((BOLD, DARKBLUE, i, END)),
                    ''.join((BOLD, DARKBLUE, 'Test', END)),
                    ''.join((BOLD, FAIL, 'Local', END)),
                ])
                projects_dictionary[idx] = {
                    'region': ['Local'],
                    'function_name': i
                }
        elif i in projects_aws_lambda:
            projects_summary.append([
                ''.join((BOLD, OKGREEN, str(idx), END)),
                ''.join((BOLD, OKGREEN, i, END)),
                ''.join((BOLD, OKGREEN, 'On AWS', END)),
                ''.join((BOLD, OKGREEN, ' '.join(projects_regions[i]), END)),
            ])
            projects_dictionary[idx] = {
                'region': projects_regions[i],
                'function_name': i
            }
            projects_regions.pop(i)
        else:
            projects_summary.append([
                ''.join((BOLD, FAIL, str(idx), END)),
                ''.join((BOLD, FAIL, i, END)),
                ''.join((BOLD, FAIL, 'Local', END)),
                ''.join((BOLD, FAIL, 'Local', END)),
            ])
            projects_dictionary[idx] = {
                'region': ['Local'],
                'function_name': i
            }
    total_local = len(projects_summary)
    for idx, i in enumerate(projects_regions.keys()):
        projects_summary.append([
            ''.join((BOLD, str(idx + total_local), END)),
            ''.join((BOLD, i, END)),
            ''.join((BOLD, 'Only AWS', END)),
            ''.join((BOLD, ' '.join(projects_regions[i]), END)),
        ])
        projects_dictionary[idx + total_local] = {
            'region': projects_regions[i],
            'function_name': i
        }
    table = tabulate(
        projects_summary,
        headers=['ID', 'PROYECTO', 'ESTADO', 'UBICACION'],
        tablefmt='orgtbl'
    )
    print table
    option = raw_input("\nSeleccione el ID de la funcion para mayores detalles: ")
    detail_aws_function(projects_dictionary, option)


def detail_aws_function(projects_dictionary={}, option='0'):
    u"""
    Muestra el detalle de una función específica
    """
    function = projects_dictionary.get(int(option))
    try:
        for i in function.get('region'):
            if i == 'Local':
                print ''

                makefile = open('/'.join(('.', function.get('function_name'), "Makefile")), "r")
                function_file = open(
                    '/'.join((
                        '.',
                        function.get('function_name'),
                        function.get('function_name'),
                        ''.join((function.get('function_name'), '.py'))
                    )),
                    "r"
                )
                data_function = {}
                for line in function_file.readlines():
                    if '__version__ = ' in line:
                        data_function['version'] = line.replace('__version__ = ', '')
                        break
                function_file.close()
                for line in makefile.readlines():
                    if 'DESCRIPTION = ' in line:
                        data_function['description'] = line.replace('DESCRIPTION = ', '')
                    elif 'RUNTIME_VERSION = ' in line:
                        data_function['runtime_version'] = line.replace('RUNTIME_VERSION = ', '')
                    elif 'TIMEOUT = ' in line:
                        data_function['timeout'] = line.replace('TIMEOUT = ', '')
                    elif 'MEMORY_SIZE = ' in line:
                        data_function['memory_size'] = line.replace('MEMORY_SIZE = ', '')
                        break
                makefile.close()
                table = tabulate(
                    [
                        [''.join((BOLD, 'UBICACION', END)), i],
                        [''.join((BOLD, 'DESCRIPCION', END)), data_function.get('description', '')],
                        [''.join((BOLD, 'RUNTIME VERSION', END)), data_function.get('runtime_version', '')],
                        [''.join((BOLD, 'MEMORY SIZE', END)), data_function.get('memory_size', '')],
                        [''.join((BOLD, 'TIMEOUT', END)), data_function.get('timeout', '')],
                        [''.join((BOLD, 'VERSION', END)), data_function.get('version', '')]
                    ],
                    headers=[''.join((BOLD, 'NOMBRE')), function.get('function_name')],
                    tablefmt="orgtbl"
                )
                print table
            else:
                client = boto3.client(
                    'lambda',
                    region_name=i,
                    aws_access_key_id=AWS_LAMBDA.get('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=AWS_LAMBDA.get('AWS_SECRET_ACCESS_KEY')
                )
                response = client.get_function_configuration(
                    FunctionName=function.get('function_name')
                )
                print ''
                table = tabulate(
                    [
                        [''.join((BOLD, 'UBICACION', END)), i],
                        [''.join((BOLD, 'DESCRIPCION', END)), response.get('Description')],
                        [''.join((BOLD, 'RUNTIME', END)), response.get('Runtime')],
                        [''.join((BOLD, 'RAM', END)), response.get('MemorySize')],
                        [''.join((BOLD, 'TIMEOUT', END)), response.get('Timeout')],
                        [''.join((BOLD, 'VERSION', END)), response.get('Version')],
                        [''.join((BOLD, 'ULTIMA MOD', END)), response.get('LastModified')]
                    ],
                    headers=[''.join((BOLD, 'NOMBRE')), response.get('FunctionName')],
                    tablefmt="orgtbl"
                )
                print table
    except:
        print BOLD, FAIL
        print '[ERROR] No es posible obtener los datos de configuracion,'
        print '        posible casos:', END
        print FAIL
        print '      - El nombre de la función no existe.'
        print '      - La ubicación de la función no es correcta.'
        print '      - No se puede acceder a los archivos de configuración.'
        print '      - El arbol de directorios no es el correcto.', END
        # print traceback.format_exc()


def view_lambda_function(args):
    u"""
    Visualiza las configuraciones de una función lambda específica.
    """
    header("CONFIGURACION DE FUNCIÓN LAMBDA")
    find = False
    region = None
    for i in args:
        for key in AWS_REGIONS.values():
            if i in key.get('region'):
                region = i
                args.remove(i)
                find = True
                break
            elif i in ['Local', 'local', 'localhost']:
                region = 'Local'
                args.remove(i)
                find = True
                break
        if find:
            break
    try:
        function_name = args[0]
        projects_dictionary = {
            0: {
                'region': [region],
                'function_name': function_name
            }
        }
        detail_aws_function(projects_dictionary)
    except:
        print traceback.format_exc()


def check_aws_lambda_function(args):
    u"""
    Revisa si una función lambda específica se encuentra el AWS Lambda.
    """
    header("REVISIÓN DE FUNCIÓN LAMBDA")


# ==============================================================================
# CREACION DE FUNCIONES PARA DESARROLLO TEST
# ==============================================================================
def test_lambda_function(args):
    u"""
    Duplicación de función lambda para desarrollo en formato test.
    """
    header("CREACION DE FUNCION TEST PARA DESARROLLO")
    projects_summary = []
    lambda_projects = []
    projects_test= []
    projects_dictionary = {}
    tmp_lambda_projects = next(walk('.'))[1]
    for i in tmp_lambda_projects:
        if i not in BLACK_LIST_DIRECTORIES:
            lambda_projects.append(i)

    for i in lambda_projects:
        if 'test' in i:
            projects_test.append(i.replace('_test', ''))
    for idx, i in enumerate(lambda_projects):
        if 'test' in i or i in projects_test:
            projects_summary.append([
                ''.join((BOLD, FAIL, str(idx), END)),
                ''.join((BOLD, FAIL, i, END)),
                ''.join((BOLD, FAIL, 'Bloqueado', END))
            ])
        else:
            projects_summary.append([
                ''.join((BOLD, OKGREEN, str(idx), END)),
                ''.join((BOLD, OKGREEN, i, END)),
                ''.join((BOLD, OKGREEN, 'Permitido', END))
            ])
            projects_dictionary[idx] = {
                'function_name': i
            }
    table = tabulate(
        projects_summary,
        headers=['ID', 'PROYECTO', 'ESTADO'],
        tablefmt='orgtbl'
    )
    print table
    option = raw_input("\nSeleccione el ID de la funcion para crear duplicado: ")
    create_duplicate_test(projects_dictionary.get(int(option), None))


def create_duplicate_test(function_name):
    u"""
    Crea la función test duplicando una función original indicada.
    """
    if function_name.get('function_name', None):
        header("DUPLICANDO FUNCION: '%s'." % (function_name.get('function_name')))
        copytree(
            ''.join((
                './', function_name.get('function_name'),
                '/', function_name.get('function_name')
            )),
            ''.join((
                './', function_name.get('function_name'), '_test',
                '/', function_name.get('function_name'), '_test/'
            ))
        )
        rename(
            ''.join((
                './', function_name.get('function_name'), '_test',
                '/', function_name.get('function_name'), '_test',
                '/', function_name.get('function_name'), '.py',
            )),
            ''.join((
                './', function_name.get('function_name'), '_test',
                '/', function_name.get('function_name'), '_test',
                '/', function_name.get('function_name'), '_test.py',
            ))
        )
        src = ''.join((
            './', function_name.get('function_name')
        ))
        dest = ''.join((
            './', function_name.get('function_name'), '_test'
        ))
        src_files = listdir(src)
        for file_name in src_files:
            try:
                full_file_name = path.join(src, file_name)
                if (path.isfile(full_file_name)):
                    copy(full_file_name, dest)
                    print ''.join((OKGREEN, "[OK] ", file_name, END))
            except:
                print ''.join((
                    FAIL,
                    "[ERROR] No fue posible duplicar el archivo ",
                    file_name,
                    END
                ))
        rewrite_makefile(function_name.get('function_name'), type_function='test')
    else:
        print ''.join((
            FAIL,
            "[ERROR] Función no reconocida o no permitida.",
            END
        ))


def rewrite_makefile(function_name, type_function=''):
    u"""
    Reescribe las configuraciones del archivo 'Makefile' para ser usado por la
    función test de lambda duplicada.
    """
    if type_function in ['test', '', 'production']:
        if type_function is 'test':
            type_function = '_test'
        with open(''.join(('./', function_name, type_function, "/Makefile")), "r+") as makefile:
            text = makefile.read()
            text = re.sub(
                'PROJECT = (\w+)',
                ''.join(('PROJECT = ', function_name, type_function)),
                text
            )
            text = re.sub(
                'FUNCTION_NAME = (\w+)',
                ''.join(('FUNCTION_NAME = ', function_name, type_function)),
                text
            )
            if type_function is '_test':
                text = re.sub(
                    'DESCRIPTION = (")',
                    'DESCRIPTION = "[TEST] ',
                    text
                )
            else:
                text = re.sub(
                    'DESCRIPTION = ("\[TEST\] )',
                    'DESCRIPTION = "',
                    text
                )
            makefile.seek(0)
            makefile.write(text)
            makefile.truncate()
            makefile.close()
    else:
        print ''.join((
            FAIL,
            "[ERROR] No fue posible reescribir el archivo 'Makefile'.",
            END
        ))


# ==============================================================================
# FUNCIONES TEST A VERSION DE PRODUCCION
# ==============================================================================
def production_lambda_function(args):
    u"""
    Pasa una función test a modo de producción.
    """
    header("PASO DE FUNCION TEST A PRODUCCION")
    projects_summary = []
    lambda_projects = []
    projects_test= []
    projects_dictionary = {}
    tmp_lambda_projects = next(walk('.'))[1]
    for i in tmp_lambda_projects:
        if i not in BLACK_LIST_DIRECTORIES:
            lambda_projects.append(i)

    for i in lambda_projects:
        if 'test' in i:
            projects_test.append(i.replace('_test', ''))
    for idx, i in enumerate(lambda_projects):
        if 'test' in i:
            projects_summary.append([
                ''.join((BOLD, OKGREEN, str(idx), END)),
                ''.join((BOLD, OKGREEN, i, END)),
                ''.join((BOLD, OKGREEN, 'Permitido', END))
            ])
            projects_dictionary[idx] = {
                'function_name': i
            }
        else:
            projects_summary.append([
                ''.join((BOLD, FAIL, str(idx), END)),
                ''.join((BOLD, FAIL, i, END)),
                ''.join((BOLD, FAIL, 'Bloqueado', END))
            ])
    table = tabulate(
        projects_summary,
        headers=['ID', 'PROYECTO', 'ESTADO'],
        tablefmt='orgtbl'
    )
    print table
    option = raw_input("\nSeleccione el ID de la funcion para transformar: ")
    test_to_production(projects_dictionary.get(int(option), None))


def test_to_production(function_name):
    u"""
    """
    if function_name.get('function_name', None):
        header("CONVIRTIENDO FUNCION: '%s'." % (function_name.get('function_name')))
        production_function_name = function_name.get('function_name').replace('_test', '')
        # print production_function_name
        copytree(
            ''.join((
                './', function_name.get('function_name'),
                '/', function_name.get('function_name')
            )),
            ''.join((
                './', production_function_name,
                '/', production_function_name
            ))
        )
        rename(
            ''.join((
                './', production_function_name,
                '/', production_function_name,
                '/', function_name.get('function_name'), '.py',
            )),
            ''.join((
                './', production_function_name,
                '/', production_function_name,
                '/', production_function_name, '.py',
            ))
        )
        src = ''.join((
            './', function_name.get('function_name')
        ))
        dest = ''.join((
            './', production_function_name
        ))
        src_files = listdir(src)
        for file_name in src_files:
            try:
                full_file_name = path.join(src, file_name)
                if (path.isfile(full_file_name)):
                    copy(full_file_name, dest)
                    print ''.join((OKGREEN, "[OK] ", file_name, END))
            except:
                print ''.join((
                    FAIL,
                    "[ERROR] No fue posible duplicar el archivo ",
                    file_name,
                    END
                ))
        rewrite_makefile(production_function_name)
    else:
        print ''.join((FAIL, "[ERROR] Función no reconocida o no permitida.", END))


# ==============================================================================
# OPCIONES DISPONIBLES
# ==============================================================================
def delete_lambda_function(args):
    u"""
    Elimina una función lambda específica.
    """
    header("ELIMINA UNA FUNCIÓN LAMBDA")


def main(arguments):
    # ==========================================================================
    # OPCIONES DISPONIBLES
    # ==========================================================================
    AVAILABLE_OPTIONS = {
        'create': create_lambda_function,
        'list': list_lambda_function,
        'view': view_lambda_function,
        'test': test_lambda_function,
        'production': production_lambda_function
        # 'delete': delete_lambda_function
    }
    # ==========================================================================
    # CARGA DE OPCIONES
    # ==========================================================================
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-c',
        '--create',
        action='store_true',
        help=''.join((
            DARKBLUE,
            "Crea una función lambda de forma interactiva.",
            END
        ))
    )
    parser.add_argument(
        '-l',
        '--list',
        action='store_true',
        help=''.join((
            OKBLUE,
            "Enlista las funciones lambda existente en localhost como en AWS Lambda",
            END
        ))
    )
    parser.add_argument(
        '-v',
        '--view',
        nargs=2,
        help=''.join((
            DARKBLUE,
            "Visualiza la configuración de una función lambda",
            END
        ))
    )
    parser.add_argument(
        '-t',
        '--test',
        action='store_true',
        help=''.join((
            OKBLUE,
            "Duplica una función lambda en modo test con todas sus configuraciones originales.",
            END
        ))
    )
    parser.add_argument(
        '-p',
        '--production',
        action='store_true',
        help=''.join((
            DARKBLUE,
            "Convierte una función de tipo test a produccion.",
            END
        ))
    )
    parser.add_argument(
        '-d',
        '--delete',
        action='store_true',
        # choices=[],
        help=''.join((OKBLUE, "Elimina una función lambda", END))
    )
    # ==========================================================================
    # SELECTOR
    # ==========================================================================
    args = parser.parse_args(arguments)
    for k in args.__dict__:
        if args.__dict__[k] not in [None, False, []]:
            if AVAILABLE_OPTIONS.get(k, None):
                AVAILABLE_OPTIONS[k](args.__dict__[k])
            else:
                print ''.join((
                    FAIL,
                    "[ERROR] Función no disponible.",
                    END
                ))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))