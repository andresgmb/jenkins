# ==============================================================================
# DATOS DEL PROYECTO
# ==============================================================================
PROJECT = $project
FUNCTION_NAME = $function_name
DESCRIPTION = "$description"
AWS_REGION = $aws_region

# ==============================================================================
# CONFIGURACIONES ESTATICAS
# ==============================================================================
VIRTUAL_ENV = env
FUNCTION_HANDLER = lambda_handler
LAMBDA_ROL = arn:aws:iam::242956272159:role/lambda_basic_execution
SETTINGS=file://secrets.json
RUNTIME_VERSION = $runtime_version
TIMEOUT = 120
MEMORY_SIZE = 128

# ==============================================================================
# CONFIGURACIONES DE COLORES
# ==============================================================================
HEADER = '\033[96m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# ==============================================================================
# DEFAULT COMMANDS
# ==============================================================================
install: virtual install_requirements
build: install clean_package build_package_tmp copy_python remove_unused zip
deploy: install build lambda_create
update: install build lambda_update
update_configuration: lambda_update_conf

clean: clean_package
	@+echo $(HEADER)"Limpando Archivos compilados"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@rm -rf ./$(FUNCTION_NAME)/*.pyc
	@+echo $(OKGREEN)"[OK] Archivos compilados eliminados."$(END)
	@+echo ""

uninstall: clean
	@+echo $(HEADER)"Desinstalando paquetes y entorno virtual"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@rm -rf ./$(VIRTUAL_ENV)
	@+echo $(OKGREEN)"[OK] Entorno virtual desinstalado"$(END)
	@rm -rf ./package
	@+echo $(OKGREEN)"[OK] Paquetes desinstalado"$(END)
	@+echo ""

virtual:
	@+echo  $(HEADER)"Instalando y activando entorno virtual"
	@+echo "---------------------------------------------"$(END)
	@+echo $(WARNING)""
	@if test ! -d "$(VIRTUAL_ENV)"; then \
		pip install virtualenv; \
		virtualenv -p python$(RUNTIME_VERSION) $(VIRTUAL_ENV); \
	fi
	@+echo ""$(END)

install_requirements: requirements
	@+echo $(HEADER)"Instalando paquetes requeridos por el entorno"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(WARNING)""
	@ $(VIRTUAL_ENV)/bin/pip install -Ur requirements
	@ touch $(VIRTUAL_ENV)/bin/activate
	@+echo $(OKGREEN)"[OK] Paquetes instalados"$(END)
	@+echo ""

clean_package:
	@rm -rf ./package/*

build_package_tmp:
	@+echo $(HEADER)"============================================="$(END)
	@+echo $(HEADER)"CONSTRUYENDO PACKAGE '"$(FUNCTION_NAME)"'" $(END)
	@+echo $(HEADER)"============================================="$(END)
	@mkdir -p ./package/tmp/lib
	@cp -a ./$(PROJECT)/. ./package/tmp/

copy_python:
	@+echo $(HEADER)"Cargando librerias"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@if test -d $(VIRTUAL_ENV)/lib; then \
		cp -a $(VIRTUAL_ENV)/lib/python$(RUNTIME_VERSION)/site-packages/. ./package/tmp/; \
	fi
	@if test -d $(VIRTUAL_ENV)/lib64; then \
		cp -a $(VIRTUAL_ENV)/lib64/python$(RUNTIME_VERSION)/site-packages/. ./package/tmp/; \
	fi
	@+echo $(OKGREEN)"[OK] Librerias cargadas"$(END)
	@+echo ""

remove_unused:
	@+echo $(HEADER)"Eliminando archivos sin uso"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@rm -rf ./package/tmp/wheel*
	@rm -rf ./package/tmp/easy-install*
	@rm -rf ./package/tmp/setuptools*
	@+echo $(OKGREEN)"[OK] Archivos eliminados"$(END)
	@+echo ""

zip:
	@+echo $(HEADER)"Empaquetando"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@if ! cd ./package/tmp && zip -q -r ../$(PROJECT).zip .; then \
		echo $(FAIL)"[ERROR] Problema en el empaquetamiento."$(END); \
	else \
		zip -q -r ../$(PROJECT).zip . ; \
		echo $(OKGREEN)"[OK] Empaquetado finalizado"$(END); \
	fi
	@+echo ""

# ==============================================================================
# LAMBDA COMMANDS
# ==============================================================================
lambda_delete:
	@+echo $(HEADER)"Eliminando función de AWS Lambda"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@if ! aws lambda delete-function \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION_NAME); then \
		echo $(FAIL)"[ERROR] No se pudo eliminar la funcion de AWS Lambda, puede que la funcion no exista"$(END);\
	else \
		echo $(OKGREEN)"[OK] Eliminación Completada"$(END); \
	fi
	@+echo ""

lambda_create:
	@+echo $(HEADER)"Creando función en AWS Lambda"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@if ! aws lambda create-function \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION_NAME) \
		--description $(DESCRIPTION) \
		--zip-file fileb://./package/$(PROJECT).zip \
		--role $(LAMBDA_ROL) \
		--handler $(PROJECT).$(FUNCTION_HANDLER) \
		--runtime python$(RUNTIME_VERSION) \
		--timeout $(TIMEOUT) \
		--memory-size $(MEMORY_SIZE) \
		--cli-input-json $(SETTINGS); then \
		echo $(FAIL)"[ERROR] Despliegue fallido, intente 'make update'"$(END);\
	else \
		echo $(OKGREEN)"[OK] Despliegue finalizado"$(END); \
	fi

lambda_update:
	@+echo $(HEADER)"Actualizando función en AWS Lambda"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@if ! aws lambda update-function-code \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION_NAME) \
		--zip-file fileb://./package/$(PROJECT).zip; then \
		echo $(FAIL)"[ERROR] Actualización fallida, intente 'make deploy'"$(END);\
	else \
		echo $(OKGREEN)"[OK] Actualización finalizada"$(END); \
	fi

lambda_update_conf:
	@+echo $(HEADER)"Actualizando configuración de función en AWS Lambda"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@if ! aws lambda update-function-configuration \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION_NAME) \
		--cli-input-json $(SETTINGS); then \
		echo $(FAIL)"[ERROR] Actualización fallida, intente 'make deploy'"$(END);\
	else \
		echo $(OKGREEN)"[OK] Actualización finalizada"$(END); \
	fi