# Obtención del identificador de cuadra de un set de coordenadas.

GetAddressBlock se conecta a un servicio de R (Rserve) es un servidor de Destácame, al que envía las coordenadas de una dirección, el CUT de la comuna y el identificador de la Región que se realizará la búsqueda. Recibe como respuesta un identificador de cuadra, que luego envía, junto con los otros datos de la dirección, a la API de Destácame para actualizar una dirección.

Para hacer una llamada, se deben enviar los siguientes datos, en formato JSON:

```
{
  "longitude": -70.6354413,
  "latitude": -33.4386086,
  "location_type": "GEOMETRIC_CENTER",
  "address": 122525,
  "reg": "Reg13",
  "cut": "13101",
  "target": "Pandora",
  "debug": true
}
```

Donde:

* `latitude`, `longitude` y `location_type` son los mismos datos obtenidos desde la API Geocode de Google Maps.
* `address` es la ID de la dirección en la base de datos de Destácame. Será el registro que se actualizará posteriormente.
* `target`, es el servidor donde se guardaran los datos. Las opciones disponibles son `Pandora`, `Ares` y `Production`.
* `reg` es el identificador de la región, debe ser enviado desde el servidor de Destácame previamente. En el modelo Region (addresses.models.Region) es el campo `r_val`.
* `cut` es el Código Único Territorial de la comuna donde se buscarán los datos. En el modelo de datos de Destácame, está en el modelo Comuna (addresses.models.Comuna), en el campo `cut`.
* `debug` es un booleano, que indicará si se imprimen todos los Logs del código, o solo aquellos indispensables.


## Construir el paquete para subir a AWS Lambda (Linux)

Además de la máquina virtual de Java (obviamente), se debe tener instalado `gradle` en el sistema, para manejar las dependencias y las tareas del proyecto, como el empaquetamiento. El proyecto debe ser creado con la siguiente estructura:

```
ProjectFolder
|-- src
|   |-- main
|       |-- java
|           |-- com
|               |-- example
|                   |-- package
|                       |-- LambdaHandlerFile.java
|                       |-- OtherClassFile.java
|                       |-- YetAnotherClassFile.java
|-- jars
|   |-- Library1.jar
|   |-- Library2.jar
|-- build.gradle
```

El código debe estar dentro de la ruta `/src/main/java/` para ser reconocido por el empaquetador. En este caso, el paquete creado es `com.example.package`, al que pertenecen los archivos .java listados. Uno de los archivo debe tener una función pública que será llamada por Lambda para iniciar la ejecución. El nombre no importa, dado que se configura en la consola de administración de AWS Lambda.

La carpeta `jars` contiene las librerías que no se pueden manejar automáticamente con Maven. La carpeta no se llama `lib` simplemente por un conflicto con el *.gitignore*, así que se optó por el nombre alternativo clásico.

`build.gradle` es el archivo que contiene la configuración de las dependencias del proyecto, y que se ocupa para hacer el empaquetamiento de la función para AWS Lambda.

Para ejecutarlo, dentro de la carpeta principal del proyecto, se ejecuta:

```
gradle build
```

Esto generará una carpeta `build` en la raíz del proyecto. En `/build/distributions/` habrá un archivo llamada `ProjectFolder.zip` que se debe subir a AWS Lambda, en el campo **Function package** de la función, en la sección **Code**.
