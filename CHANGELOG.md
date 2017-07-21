<!--
IMPACTO.
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

Versionamiento
A.B.C

A: Cambio sustancial en la estructura o en la manera de operar la aplicación.
B: Nuevas carácteristicas, nuevas funcionalidades y conjunto de grandes correcciones.
C: Correcciones de bugs de la serie B.
-->

# Change Log

## [0.2.0] 2017-06-16

### Added
- [FEATURE] Nuevo parámetro para duplicar una función lambda descargada y cargarla en modo test.
- [FEATURE] Ver detalles de configuración de una función lambda directamente desde el manager usando el comando python manage.py -v <region> <nombre_funcion>.
- [FEATURE] Ver detalles de configuración de una función lambda desplegada en AWS Lambda o alojada en local.
- [FEATURE] Detecta las funciones tanto locales como desplegadas en AWS Lambda para ser enlistadas.
- [FEATURE] Listado de funciones lambda, detecta la region y el estado de la función.
- [PROJECT] Versión 0.2.0 de módulo de 'manage.py'.

### Changed
- [DEV] Nuevas variables para los makefiles, 'MEMORY_SIZE' y 'TIMEOUT'.
- [DEV] Cambio en el nombre de variable para el runtime de los makefiles.
