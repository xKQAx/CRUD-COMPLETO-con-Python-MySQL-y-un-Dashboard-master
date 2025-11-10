# Comandos para Iniciar la Aplicación

## Navegar al directorio de la aplicación

Desde el directorio raíz del proyecto:

```bash

cd my-app

```

## Ejecutar la aplicación

### Opción 1: Desde el directorio my-app

```bash
cd my-app
python run.py
```

## Acceder a la aplicación

Una vez ejecutada, la aplicación estará disponible en:

```
http://127.0.0.1:5600/
```

## Activar entorno virtual (si es necesario)

### Windows PowerShell

```bash
.\env\Scripts\Activate.ps1
```

### Windows CMD

```bash
.\env\Scripts\activate.bat
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Crear la base de datos

Ejecuta el script para crear la base de datos directamente:

```bash
python crear_bd.py
```

Este script creará la base de datos `crud_python` y todas sus tablas. Luego podrás conectarte con tu Database Client usando:

- Host: localhost
- Usuario: root
- Contraseña: password (edita crear_bd.py si tu contraseña es diferente)
- Base de datos: crud_python
- Puerto: 3306

