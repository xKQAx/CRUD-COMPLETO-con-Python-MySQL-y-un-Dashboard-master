"""
Script para crear la base de datos crud_python directamente desde el archivo SQL
Ejecuta este script para crear la base de datos y luego podrás conectarte con tu Database Client

CONFIGURACION:
Las credenciales se leen desde el archivo .env
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de conexión MySQL - Se lee desde .env
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'crud_python')

def crear_base_datos():
    print("=" * 60)
    print(f"CREANDO BASE DE DATOS {MYSQL_DATABASE}")
    print("=" * 60)
    
    # Leer el archivo SQL
    sql_file_path = os.path.join('my-app', 'BD', 'crud_python.sql')
    
    if not os.path.exists(sql_file_path):
        print(f"Error: No se encontró el archivo {sql_file_path}")
        return False
    
    try:
        # Conectar a MySQL sin especificar la base de datos
        print("\n1. Conectando a MySQL...")
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            port=MYSQL_PORT,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        
        if connection.is_connected():
            print("   Conexión exitosa a MySQL")
            
            cursor = connection.cursor()
            
            # Leer el archivo SQL
            print("\n2. Leyendo archivo SQL...")
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()
            
            # Ejecutar el script SQL
            print("\n3. Ejecutando script SQL...")
            
            # Ejecutar múltiples comandos usando execute con multi=True
            try:
                for result in cursor.execute(sql_script, multi=True):
                    if result.with_rows:
                        result.fetchall()
                connection.commit()
                print("   Script SQL ejecutado correctamente")
            except mysql.connector.Error as e:
                # Si falla con multi=True, intentar ejecutar comandos individuales
                print("   Ejecutando comandos individualmente...")
                commands = []
                current_command = ""
                in_string = False
                string_char = None
                
                for line in sql_script.split('\n'):
                    stripped = line.strip()
                    if not stripped or stripped.startswith('--') or stripped.startswith('/*'):
                        continue
                    
                    for char in line:
                        if char in ("'", '"', '`') and (not current_command or current_command[-1] != '\\'):
                            if not in_string:
                                in_string = True
                                string_char = char
                            elif char == string_char:
                                in_string = False
                                string_char = None
                        
                        current_command += char
                        
                        if char == ';' and not in_string:
                            cmd = current_command.strip()
                            if cmd:
                                commands.append(cmd)
                            current_command = ""
                
                if current_command.strip():
                    commands.append(current_command.strip())
                
                for cmd in commands:
                    if cmd.strip():
                        try:
                            cursor.execute(cmd)
                            connection.commit()
                        except mysql.connector.Error as e:
                            error_msg = str(e).lower()
                            if "already exists" not in error_msg and "unknown database" not in error_msg:
                                print(f"   Advertencia: {e}")
            
            # Verificar que la base de datos fue creada
            print("\n4. Verificando creación de la base de datos...")
            cursor.execute(f"SHOW DATABASES LIKE '{MYSQL_DATABASE}'")
            result = cursor.fetchone()
            
            if result:
                print(f"   Base de datos '{MYSQL_DATABASE}' creada exitosamente")
                
                # Verificar tablas
                cursor.execute(f"USE {MYSQL_DATABASE}")
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                if tables:
                    print(f"   Tablas creadas: {len(tables)}")
                    for table in tables:
                        print(f"   - {table[0]}")
                else:
                    print("   Advertencia: No se encontraron tablas")
            else:
                print("   Error: No se pudo crear la base de datos")
                return False
            
            cursor.close()
            connection.close()
            
            print("\n" + "=" * 60)
            print("Base de datos creada exitosamente")
            print("=" * 60)
            print("\nAhora puedes conectarte con tu Database Client usando:")
            print(f"  Host: {MYSQL_HOST}")
            print(f"  Usuario: {MYSQL_USER}")
            print(f"  Contraseña: {MYSQL_PASSWORD}")
            print(f"  Base de datos: {MYSQL_DATABASE}")
            print(f"  Puerto: {MYSQL_PORT}")
            print("=" * 60)
            
            return True
        else:
            print("Error: No se pudo establecer la conexión")
            return False
            
    except mysql.connector.Error as error:
        print(f"\nError de conexión: {error}")
        print("\nPosibles soluciones:")
        print("  1. Verifica que MySQL esté corriendo")
        print("  2. Revisa usuario y contraseña en el archivo .env")
        print(f"  3. Asegúrate de que el puerto MySQL ({MYSQL_PORT}) esté disponible")
        return False
        
    except FileNotFoundError:
        print(f"\nError: No se encontró el archivo {sql_file_path}")
        print("Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return False
        
    except Exception as e:
        print(f"\nError inesperado: {e}")
        return False

if __name__ == "__main__":
    crear_base_datos()

