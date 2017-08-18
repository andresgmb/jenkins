# Jenkins – Instalacion y logica de funciones Lambda


## 1. Instalacion Jenkins [![N|Solid](http://i.imgur.com/2WRpzsb.png)]

Jenkins corre sobre un servidor Linux, y se recomienda con requerimientos minimos 1 GB ram y 10 GB de almacenamiento, estos requerimientos varian según las actividades que pensemos operar alli. Una vez tengamos la maquina preparada, instalar:

  - **Python(Verificar que pip este instalado y actualizado)**
  - **Virtualenv:**
    ```sh
    $ sudo pip install virtualenv
    ```
  - **Git:**
    ```sh
    $ sudo apt-get update
    $ sudo apt-get install git
    ```
  - **Java:**
    ```sh
    $ sudo apt-get update
    $ sudo apt-get install openjdk-8-jdk
    $ java -version # Solo para verificar si quedo instalado
    $ vim /etc/profile # Abre archivo para setear JAVA_HOME
    ```
    Al final del alrchivo escribir:
    ```sh
    JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
    export JAVA_HOME
    export PATH=$PATH:$JAVA_HOME/bin
    ```
    Guardar y salir, luego:
    ```sh
    $ source /etc/profile # Para activar sin reiniciar, comprobar con echo $JAVA_HOME
    ```
  - **Jenkins:**
    ```sh
    $ sudo apt-get update
    $ sudo wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | apt-key add -
    $ sudo apt-get update
    $ sudo apt-get install jenkins
    $ sudo service jenkins status # Para verificar si ya esta todo Ok
    ```
  - **AWS Cli:**
    ```sh
    $ sudo pip install awscli
    $ aws --version # Verifica que se instalo y retorna la version instalada
    $ aws configure # Esto nos solicita lo siguiente
       AWS Access Key ID [None]: # AKIAIOSFODNN7EXAMPLE
       AWS Secret Access Key [None]: # wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY  
       Default region name [None]: # us-west-2  
       Default output format [None]: # json
    ```
  - **Hub:**
    ```sh
    $ sudo dnf install hub
    $ hub version # Verifica que se instalo y retorna la version instalada
    ```
  - **zip unzip:**
    ```sh
    $ sudo apt-get update
    $ sudo apt-get install zip unzip
    ```
  - **Gradle:**
    ```sh
    $ sudo apt-get update
    $ wget https://services.gradle.org/distributions/gradle-3.4.1-bin.zip
    $ sudo mkdir /opt/gradle
    $ sudo unzip -d /opt/gradle gradle-3.4.1-bin.zip
    $ export PATH=$PATH:/opt/gradle/gradle-3.4.1/bin
    $ gradle -v  # Verifica que se instalo y retorna la version instalada
    ```
  - **Clave SSH para Git (Hacerlo con usuario Jenkins):**
    ```sh
    $ cd ~/.ssh/
    $ ssh-keygen # Eligir si es id_rsa u otro archivo y elegir una clave, esto genera dos archivos, privado y publico
    $ cat id_rsa.pub # Copiar el contenido que arroja por consola
    ```
    Ir a GitHub y pegar este contenido cuando generes un SSH nuevo
  - **Configurar GnuPG para encriptar archivos secrets:**
  
    Este proceso se lleva acabo desde el servidor Jenkins con el usuario jenkins, si el servidor no cuenta con suficiente memoria RAM no podra generar una llave de 3072 bits, dado el caso generarla en otro computador y exportar ambas claves (publica y privada) e importarlas en el servidor.
    ```sh
    $ gpg --gen-key # Generar claves publicas y privadas
       Tipo: Elegir opcion 2 DSA and Elgamal
       Longitud de bits: 3072 (Si se tiene un equipo con poca memoria no va a soportar los 3072)
       Expira: 0 (Nunca expira)
       Nombre: Destacame-Jenkins
       Correo: destacame@destacame.cl
       Comentario: Usado para cifrar el secret
       Enter passphrase (Y confirmar): ******
    $ gpg --list-keys # Ver la lista de las claves y copiar el Id de la llave publica
    $ gpg --output publickey.gpg --export 9AE482C0 # 9AE482C0 es el Id de la llave publica
    ```
    Una vez generado el archivo publickey.gpg, distribuirlo a todo el que lo requiera (Esta llave solo sirve para encriptar, no representa ninguna vulnerabilidad el que sea de dominio publico), dentro del repositorio en la carpeta template se dejara una copia de la llave. El usuario que lo implemente debera hacer lo siguiente:
    ```sh
    $ gpg --import publickey.gpg   
    $ gpg --encrypt --recipient 9AE482C0 secrets.json # 9AE482C0 es el Id de la llave publica (gpg --list-keys para ver)
    ```
  - **Instalar Plugin:**
      - Ir a Manage Jenkins -> Manage Plugins -> Available
      - Buscar he instalar los siguientes plugins (Algunos vienen por defecto):
          - AnsiColor 
          - build timeout plugin 
          - Conditional BuildStep 
          - Credentials Plugin 
          - Git plugin 
          - GitHub Plugin 
          - GitHub Branch Source Plugin 
          - GitHub Integration Plugin 
          - GitHub Pull Request Builder 
          - Javadoc Plugin 
          - JUnit Plugin 
          - Safe Restart Plugin 
          - Slack Notification Plugin 
          - Slack Upload Plugin 
          - Workspace Cleanup Plugin 
   - **Configurar Salck:**
      - Ir a Manage Jenkins -> Configure System -> Global Slack Notifier Settings
      - Llenar los campos:
          - Team Subdomain: destacame
          - Integration Token Credential ID: Aggregar una credencial tipo secret, con los siguientes valores; Scope: Global, Secret: Token generado en Slack, ID: destacame, Description: SlackToken
          - Chanel: #Jenkins
      - Hacer Test Connection y verificar en Slack en el canal Jenkins tiene un mensaje de prueba satisfactorio

## 2. Configuracion GitHub [![N|Solid](http://i.imgur.com/6D60sxm.png)]

En GitHub se deben hacer las siguientes configuraciones:

  - destacame/legolambda→ Settings → Integrations & services → Add service. Alli buscar Jenkins (GitHub plugin) y en el campo Jenkins hook url colocar la direccion del servidor Jenkins, ejemplo; http://serveramazon.com:8080/github-webhook/  
  - En https://github.com/settings/profile de destacame, ir a Personal access tokens → Generate new token. El token que genere va a ser usado dentro de la logica del Script de Jenkins, para modificar los status con iconos dentro de GitHub.
  - En https://github.com/settings/profile de destacame, ir a SSH and GPG keys → New SSH key, de titulo ponle algo como “jenkins” y en key colocar el ssh-rsa generado dentro de Jenkis.
  - En el proyecto se deben tener 3 ramas; master, dev y qa


## 3. Configuracion Slack [![N|Solid](http://i.imgur.com/iMQlwBw.png)]

En Slack se deben hacer las siguientes configuraciones:

  - Crear un canal llamado "#Jenkins"
  - Ir a https://destacame.slack.com/apps/A0F7VRFKN-jenkins-ci y darle "Add Configuration", alli llener los siguientes campos:
    - Post to Channel: #Jenkins (O el nombre que le distes en el paso anterior)
    - Token: Este es autogenerado, copiarlo y usarlo en Jenkins en el plugin de slack
    - Descriptive Label: destacame
    - Customize Name:  destacame
    
## 4. Logica Jenkins [![N|Solid](http://i.imgur.com/jrKbgzp.png)]
El flujo de trabajo consiste en probar automaticamente a traves de Jenkins todas la funciones que se suban al repositorio GitHub y hacer Pull Request a su siguiente rama en caso de que la prueba sea exitosa. Si el Pull Request generado por Jenkins es aceptado en la rama principal (master) automaticamente se hace el despligue de crear o actualizar la funcion en aws lambda. A continuacion se detalla el proceso.

 ![N|Solid](http://i.imgur.com/BCLeAPg.png)

Este proceso se hace entre las ramas QA a Dev y Dev a Master, ver imagen:

 ![N|Solid](http://i.imgur.com/yB7X2Ua.png)

## 5. Estructura de carpetas en el repositorio [![N|Solid](http://i.imgur.com/tPvWxEr.png)]
Las funciones lambda estan en direcctorio con multiples carpetas y archivos, la siguiente es su estructura:

 ![N|Solid](http://i.imgur.com/KuPE8SU.png)

Los secrets.json.gpg no son obligatorios, si una funcion no requiere de este archivo simplemente no incluir.

## 6. Configuraciones de las tareas [![N|Solid](http://i.imgur.com/GQxl6Vi.png)]
El proceso en general consta de 3 tareas:

  - **1-Test_PR_qa_to_dev**
      - General -> GitHub project, darle check y los campos internos llenar asi:
          - Project url: git@github.com: destacame/legolambda.git
          - Display name: destacame/legolambda
      -  General -> Source Code Management, darle chek a git y los campos internos llenar asi:
          - Repository URL: git@github.com: destacame/legolambda.git
          - Credentials: Agregar las credenciales del usuario destacamebot en modo Global
          - Branch Specifier: refs/heads/qa
          - Repository browser: Seleccionar githubweb
          - URL: https://github.com/destacame/legolambda/tree/qa
      - General -> Build Triggers, darle chek a GitHub hook trigger for GITScm polling.
      - General -> Build Environment, darle chek a Delete workspace before build starts
      - General -> Build Environment, darle chek a Color ANSI Console Output y seleccionar en ANSI color map gnome-terminal
      - General -> Build, en "Add build step" seleccionar "Execute shell". Este Shell es el que genera todo el trabajo. Esto evalua cada una de las funciones agregadas y/o modificadas en la rama qa, si el resultado es exitoso hace un pull request a la rama dev. Tambien agrega estatus a los commits de GitHub en forma de iconos.
      - General -> Post-build Actions, en "Add post-build actions" seleccionar Slack Notifications, alli seleccionar la notificaciones que deseamos recibir por slack.

  - **2-PR_dev_to_master**
      - General -> GitHub project, darle check y los campos internos llenar asi:
          - Project url: git@github.com:destacame/legolambda.git
          - Display name: destacame/legolambda
      -  General -> Source Code Management, darle chek a git y los campos internos llenar asi:
          - Repository URL: git@github.com:destacame/legolambda.git
          - Credentials: Agregar las credenciales del usuario destacamebot en modo Global
          - Branch Specifier: refs/heads/dev
          - Repository browser: Seleccionar githubweb
          - URL: https://github.com/destacame/legolambda/tree/dev
      - General -> Build Triggers, darle chek a GitHub hook trigger for GITScm polling.
      - General -> Build Environment, darle chek a Delete workspace before build starts
      - General -> Build Environment, darle chek a Color ANSI Console Output y seleccionar en ANSI color map gnome-terminal
      - General -> Build, en "Add build step" seleccionar "Execute shell". Este Shell es el que genera todo el trabajo. Esto evalua cada una de las funciones aceptadas en el pull request de la rama qa a dev, si el resultado es exitoso hace un pull request a la rama master. Tambien agrega estatus a los commits de GitHub en forma de iconos.
      - General -> Post-build Actions, en "Add post-build actions" seleccionar Slack Notifications, alli seleccionar la notificaciones que deseamos recibir por slack.

  - **3-DP_master_to_aws**
      - General -> GitHub project, darle check y los campos internos llenar asi:
          - Project url: git@github.com:destacame/legolambda.git
          - Display name: destacame/legolambda
      -  General -> Source Code Management, darle chek a git y los campos internos llenar asi:
          - Repository URL: git@github.com:destacame/legolambda.git
          - Credentials: Agregar las credenciales del usuario destacamebot en modo Global
          - Branch Specifier: refs/heads/master
          - Repository browser: Seleccionar githubweb
          - URL: https://github.com/destacame/legolambda/tree/master
      - General -> Build Triggers, darle chek a GitHub hook trigger for GITScm polling.
      - General -> Build Environment, darle chek a Delete workspace before build starts
      - General -> Build Environment, darle chek a Color ANSI Console Output y seleccionar en ANSI color map gnome-terminal
      - General -> Build, en "Add build step" seleccionar "Execute shell". Este Shell es el que genera todo el trabajo. Esto evalua cada una de las funciones aceptadas en el pull request de la rama dev a master, si el resultado es exitoso evalua en aws si las funciones son nuevas o si ya existen y según se el caso el script crea o actualiza la funcion aws lambda. El metodo para determinar los parametros del deploy los toma del Makefile que se encuentra en la funcion.
      - General -> Post-build Actions, en "Add post-build actions" seleccionar Slack Notifications, alli seleccionar la notificaciones que deseamos recibir por slack.
