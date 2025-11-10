# Guía Completa de Instalación y Configuración

Esta guía te ayudará a configurar el proyecto CRUD con Python, MySQL y Dashboard desde cero.

## Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Descargar el Proyecto](#descargar-el-proyecto)
3. [Instalar Python](#instalar-python)
4. [Crear Entorno Virtual](#crear-entorno-virtual)
5. [Instalar Dependencias](#instalar-dependencias)
6. [Instalar MySQL](#instalar-mysql)
7. [Configurar MySQL](#configurar-mysql)
8. [Configurar Variables de Entorno](#configurar-variables-de-entorno)
9. [Crear Base de Datos](#crear-base-de-datos)
10. [Ejecutar la Aplicación](#ejecutar-la-aplicación)
11. [Verificar Instalación](#verificar-instalación)

## Descargar el Proyecto

### Opción 1: Clonar desde Git

Si tienes Git instalado, abre PowerShell o CMD y ejecuta:

```bash
git clone https://github.com/urian121/CRUD-COMPLETO-con-Python-MySQL-y-un-Dashboard.git
cd CRUD-COMPLETO-con-Python-MySQL-y-un-Dashboard
```

### Opción 2: Descargar ZIP

1. Ve al repositorio: https://github.com/urian121/CRUD-COMPLETO-con-Python-MySQL-y-un-Dashboard
2. Haz clic en "Code" > "Download ZIP"
3. Extrae el archivo ZIP en la ubicación deseada
4. Abre PowerShell o CMD en la carpeta extraída

---

## Instalar Python

1. Descarga Python desde: https://www.python.org/downloads/
2. Durante la instalación, marca la opción "Add Python to PATH"
3. Verifica la instalación ejecutando:

```bash
python --version
```

Deberías ver algo como: `Python 3.x.x`

---

## Crear Entorno Virtual

Un entorno virtual aísla las dependencias del proyecto. Sigue estos pasos:

1. Abre PowerShell o CMD en la carpeta del proyecto
2. Crea el entorno virtual:

```bash
python -m venv env
```

3. Activa el entorno virtual:

**En PowerShell:**
```bash
.\env\Scripts\Activate.ps1
```

Si obtienes un error de política de ejecución, ejecuta primero:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**En CMD:**
```bash
.\env\Scripts\activate.bat
```

Cuando el entorno virtual esté activo, verás `(env)` al inicio de la línea de comandos.

---

## Instalar Dependencias

Con el entorno virtual activado, instala las dependencias:

```bash
pip install -r requirements.txt
```

Esto instalará todas las librerías necesarias:
- Flask
- mysql-connector-python
- python-dotenv
- openpyxl
- Y otras dependencias

Verifica que se instalaron correctamente:

```bash
pip list
```

---

## Instalar MySQL

### Paso 1: Descargar MySQL

1. Ve a: https://downloads.mysql.com/archives/community/
2. En "Product Version", selecciona una versión estable (recomendado: 8.0.x o 8.4.x)
3. En "Operating System", selecciona "Microsoft Windows"
4. En "OS Version", selecciona "All Windows (x86, 64-bit)"
5. Descarga el archivo "Windows (x86, 64-bit), MSI Installer"

### Paso 2: Instalar MySQL

1. Ejecuta el instalador descargado (archivo .msi)
2. Selecciona "Developer Default" o "Server only"
3. Sigue el asistente de instalación
4. Cuando te pida configurar el servidor:
   - **Puerto:** 3306 (por defecto)
   - **Configuración:** Development Computer
   - **Autenticación:** Use Strong Password Encryption
5. Establece una contraseña para el usuario root (anótala, la necesitarás después)
6. Marca "Start MySQL Server at System Startup" para que inicie automáticamente
7. Completa la instalación

### Paso 3: Verificar Instalación

1. Abre el Administrador de Servicios de Windows:
   - Presiona `Win + R`
   - Escribe: `services.msc`
   - Presiona Enter
2. Busca el servicio "MySQL" o "MySQL80" o "MySQL94"
3. Verifica que el estado sea "En ejecución"
4. Si no está corriendo, haz clic derecho > "Iniciar"

---

## Configurar MySQL

### Opción 1: Usar la Contraseña que Estableciste

Si ya estableciste una contraseña durante la instalación, úsala directamente.

### Opción 2: Cambiar la Contraseña (Opcional)

Si quieres usar la contraseña por defecto "password", puedes cambiarla:

1. Abre PowerShell como Administrador
2. Ejecuta:

```bash
mysql -u root -p
```

3. Ingresa tu contraseña actual
4. Ejecuta:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
EXIT;
```

---

## Configurar Variables de Entorno

El proyecto usa un archivo `.env` para almacenar las credenciales de MySQL de forma segura.

### Paso 1: Crear el Archivo .env

1. En la raíz del proyecto, crea un archivo llamado `.env`
2. Copia el contenido de `.env.example` o crea el archivo con este contenido:

```env
# Configuración de MySQL
# Edita estos valores según tu configuración de MySQL

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_PORT=3306
MYSQL_DATABASE=crud_python
```

### Paso 2: Editar las Credenciales

Abre el archivo `.env` y edita los valores según tu configuración:

- **MYSQL_HOST:** Generalmente `localhost`
- **MYSQL_USER:** Generalmente `root`
- **MYSQL_PASSWORD:** La contraseña que estableciste para MySQL (o `password` si la cambiaste)
- **MYSQL_PORT:** Generalmente `3306`
- **MYSQL_DATABASE:** `crud_python` (se creará automáticamente)

### Paso 3: Verificar el Archivo .env

Asegúrate de que el archivo `.env` esté en la raíz del proyecto, al mismo nivel que `run.py` y `requirements.txt`.

---

## Crear Base de Datos

Una vez configurado MySQL y el archivo `.env`, crea la base de datos:

1. Asegúrate de que el entorno virtual esté activado
2. Asegúrate de que MySQL esté corriendo
3. Ejecuta el script de creación de base de datos:

```bash
python crear_bd.py
```

Este script:
- Se conectará a MySQL usando las credenciales del archivo `.env`
- Creará la base de datos `crud_python`
- Creará todas las tablas necesarias
- Insertará datos de ejemplo

Si todo sale bien, verás mensajes de confirmación.

### Solución de Problemas

Si obtienes un error de conexión:

1. Verifica que MySQL esté corriendo (Administrador de Servicios)
2. Verifica que las credenciales en `.env` sean correctas
3. Verifica que el puerto 3306 esté disponible
4. Ejecuta el script de verificación:

```bash
python verificar_mysql.py
```

---

## Ejecutar la Aplicación

Una vez completados todos los pasos anteriores:

1. Asegúrate de que el entorno virtual esté activado
2. Asegúrate de que MySQL esté corriendo
3. Ejecuta la aplicación:

```bash
python run.py
```

Deberías ver un mensaje similar a:

```
 * Running on http://127.0.0.1:5600
 * Debug mode: on
```

4. Abre tu navegador y ve a:

```
http://127.0.0.1:5600
```

---

## Verificar Instalación

### Verificar Conexión a MySQL

Ejecuta el script de verificación:

```bash
python verificar_mysql.py
```

Este script verificará:
- Que MySQL esté corriendo
- Que la conexión funcione
- Que la base de datos exista
- Que las tablas estén creadas

### Verificar la Aplicación

1. Abre el navegador en: http://127.0.0.1:5600
2. Deberías ver la página de login
3. Crea una cuenta nueva haciendo clic en "Registrarse"
4. Inicia sesión con la cuenta creada
5. Deberías ver el dashboard principal

---

## Estructura del Proyecto

```
CRUD-COMPLETO-con-Python-MySQL-y-un-Dashboard/
│
├── my-app/                    # Aplicación principal
│   ├── app.py                # Configuración de Flask
│   ├── run.py                # Script de inicio (interno)
│   ├── conexion/             # Módulo de conexión a BD
│   ├── controllers/          # Lógica de negocio
│   ├── routers/              # Rutas de la aplicación
│   ├── templates/            # Plantillas HTML
│   ├── static/               # Archivos estáticos (CSS, JS, imágenes)
│   └── BD/                   # Scripts SQL
│
├── docs/                      # Documentación
│   ├── CHANGELOG.md
│   ├── COMANDOS.md
│   ├── CONFIGURACION_ENV.md
│   └── INSTRUCCIONES_MYSQL.md
│
├── resources/                 # Recursos adicionales
│   └── template-sneat-1.0.0.zip
│
├── env/                       # Entorno virtual (no subir a Git)
├── .env                       # Variables de entorno (no subir a Git)
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Archivos ignorados por Git
├── requirements.txt          # Dependencias del proyecto
├── run.py                    # Script principal de inicio
├── crear_bd.py               # Script para crear la base de datos
├── verificar_mysql.py         # Script para verificar MySQL
├── README.md                  # Documentación principal
└── GUIA_INSTALACION.md        # Esta guía
```

---

## Comandos Útiles

### Activar Entorno Virtual

**PowerShell:**
```bash
.\env\Scripts\Activate.ps1
```

**CMD:**
```bash
.\env\Scripts\activate.bat
```

### Desactivar Entorno Virtual

```bash
deactivate
```

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Crear Base de Datos

```bash
python crear_bd.py
```

### Verificar MySQL

```bash
python verificar_mysql.py
```

### Ejecutar Aplicación

```bash
python run.py
```

### Ver Dependencias Instaladas

```bash
pip list
```

---

## Solución de Problemas Comunes

### Error: "No se puede conectar a MySQL"

**Solución:**
1. Verifica que MySQL esté corriendo (Administrador de Servicios)
2. Verifica las credenciales en el archivo `.env`
3. Verifica que el puerto 3306 esté disponible
4. Ejecuta `python verificar_mysql.py` para más detalles

### Error: "ModuleNotFoundError"

**Solución:**
1. Asegúrate de que el entorno virtual esté activado
2. Reinstala las dependencias: `pip install -r requirements.txt`

### Error: "No se puede establecer la conexión a la BD"

**Solución:**
1. Verifica que MySQL esté corriendo
2. Verifica que el archivo `.env` exista y tenga las credenciales correctas
3. Verifica que la base de datos `crud_python` exista (ejecuta `python crear_bd.py`)

### Error de Política de Ejecución en PowerShell

**Solución:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### El Puerto 5600 ya está en uso

**Solución:**
1. Cierra otras instancias de la aplicación
2. O cambia el puerto en `run.py` (última línea)

---

## Próximos Pasos

Una vez que la aplicación esté corriendo:

1. Explora el dashboard
2. Crea usuarios y empleados
3. Revisa el código en `my-app/` para entender la estructura
4. Personaliza según tus necesidades

---

## Notas Importantes

- El archivo `.env` contiene credenciales sensibles, nunca lo subas a Git
- El archivo `.env.example` es una plantilla segura para compartir
- El entorno virtual `env/` tampoco debe subirse a Git
- Siempre activa el entorno virtual antes de trabajar en el proyecto

---

## Soporte

Si encuentras problemas:

1. Revisa esta guía completa
2. Revisa los archivos en la carpeta `docs/`
3. Verifica los logs de la aplicación en la consola
4. Ejecuta `python verificar_mysql.py` para diagnosticar problemas de MySQL

---

## Referencias

- MySQL Downloads: https://downloads.mysql.com/archives/community/
- Python Downloads: https://www.python.org/downloads/
- Flask Documentation: https://flask.palletsprojects.com/
- MySQL Connector Python: https://dev.mysql.com/doc/connector-python/

---

¡Listo! Ahora deberías tener el proyecto completamente configurado y funcionando.

