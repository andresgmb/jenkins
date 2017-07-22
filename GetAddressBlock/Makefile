# ==============================================================================
# DATOS DEL PROYECTO
# ==============================================================================
PROJECT = GetAddressBlock
FUNCTION_NAME = GetAddressBlock
DESCRIPTION = "Obtención del identificador de cuadra de un set de coordenadas."
AWS_REGION = sa-east-1

# ==============================================================================
# CONFIGURACIONES ESTATICAS
# ==============================================================================
FUNCTION_HANDLER = lambda_handler
LAMBDA_ROL = arn:aws:iam::242956272159:role/lambda_basic_execution
RUNTIME_VERSION = java8
TIMEOUT = 120
MEMORY_SIZE = 128

# ==============================================================================
# CONFIGURACIONES DE COLORES
# ==============================================================================
HEADER = '\033[96m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'
END = '\033[0m'

# ==============================================================================
# DEFAULT COMMANDS   Limpiar, Armar, Construir
# ==============================================================================
deploy: clean assemble construir lambda_create clean
update: clean assemble construir lambda_update clean

clean:
	@+echo $(HEADER)"Limpando Archivos"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@gradle -q clean
	@+echo $(OKGREEN)"[OK] Archivos limpiados."$(END)
	@+echo ""

assemble:
	@+echo $(HEADER)"Armando Proyecto"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@gradle -q assemble
	@+echo $(OKGREEN)"[OK] Proyecto armado."$(END)
	@+echo ""

construir:
	@+echo $(HEADER)"Construyendo Proyecto"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@gradle -q build
	@+echo $(OKGREEN)"[OK] Proyecto construido y empaquetado."$(END)
	@+echo ""

# ==============================================================================
# LAMBDA COMMANDS
# ==============================================================================
lambda_create:
	@+echo $(HEADER)"Creando función Java en AWS Lambda"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@if ! aws lambda create-function \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION_NAME) \
		--description $(DESCRIPTION) \
		--zip-file fileb://./build/distributions/$(PROJECT).zip \
		--role $(LAMBDA_ROL) \
		--handler $(PROJECT).$(FUNCTION_HANDLER) \
		--runtime $(RUNTIME_VERSION) \
		--timeout $(TIMEOUT) \
		--memory-size $(MEMORY_SIZE); then \
		echo $(FAIL)"[ERROR] Despliegue fallido, intente 'make update'"$(END);\
	else \
		echo $(OKGREEN)"[OK] Despliegue finalizado"$(END); \
	fi

lambda_update:
	@+echo $(HEADER)"Actualizando función Java en AWS Lambda"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@if ! aws lambda update-function-code \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION_NAME) \
		--zip-file fileb://./build/distributions/$(PROJECT).zip; then \
		echo $(FAIL)"[ERROR] Actualización fallida, intente 'make deploy'"$(END);\
	else \
		echo $(OKGREEN)"[OK] Actualización finalizada"$(END); \
	fi