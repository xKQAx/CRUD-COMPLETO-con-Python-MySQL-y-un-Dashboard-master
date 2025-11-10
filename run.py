# Configurando el path para importar desde my-app
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener la ruta del directorio my-app
base_dir = os.path.dirname(os.path.abspath(__file__))
my_app_path = os.path.join(base_dir, 'my-app')

# Agregar el directorio my-app al path de Python
if my_app_path not in sys.path:
    sys.path.insert(0, my_app_path)

# Cambiar el directorio de trabajo a my-app para que Flask encuentre templates y static
os.chdir(my_app_path)

# Ahora importar la aplicación Flask
from app import app

# Configurar Flask para que busque templates y static en my-app
app.template_folder = os.path.join(my_app_path, 'templates')
app.static_folder = os.path.join(my_app_path, 'static')

# Importando todos los Routers (Rutas)
from routers.router_login import *
from routers.router_home import *
from routers.router_documentos import *
from routers.router_page_not_found import *

# Ejecutando el objeto Flask
if __name__ == '__main__':
    app.run(debug=True, port=5600)

