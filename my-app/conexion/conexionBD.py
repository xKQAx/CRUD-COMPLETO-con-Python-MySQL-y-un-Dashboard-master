

# Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
# Buscar .env en el directorio raíz del proyecto (subir dos niveles desde my-app/conexion)
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(base_dir, '.env')
load_dotenv(env_path)


def connectionBD():
    try:
        # Obtener variables de entorno
        host = os.getenv('MYSQL_HOST', 'localhost')
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', 'password')
        database = os.getenv('MYSQL_DATABASE', 'crud_python')
        port = int(os.getenv('MYSQL_PORT', '3306'))
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database,
            port=port,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )
        if connection.is_connected():
            # print("Conexión exitosa a la BD")
            return connection
        else:
            print("No se pudo establecer la conexión a la BD")
            return None

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")
        return None
    except Exception as e:
        print(f"Error inesperado al conectar: {e}")
        return None
