"""
Script de prueba para verificar la conexión a MySQL
Ejecuta este script para verificar que tu configuración de base de datos es correcta
"""

import mysql.connector
from conexion.conexionBD import connectionBD

def test_conexion():
    print("=" * 50)
    print("PRUEBA DE CONEXIÓN A MYSQL")
    print("=" * 50)
    
    try:
        print("\n1. Intentando conectar a MySQL...")
        connection = connectionBD()
        
        if connection and connection.is_connected():
            print("✅ ¡Conexión exitosa!")
            
            # Obtener información de la conexión
            db_info = connection.get_server_info()
            print(f"   - Versión del servidor MySQL: {db_info}")
            
            cursor = connection.cursor()
            
            # Verificar si la base de datos existe
            print("\n2. Verificando base de datos 'crud_python'...")
            cursor.execute("SHOW DATABASES LIKE 'crud_python'")
            result = cursor.fetchone()
            
            if result:
                print("   ✅ Base de datos 'crud_python' encontrada")
                
                # Verificar tablas
                print("\n3. Verificando tablas...")
                cursor.execute("USE crud_python")
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                if tables:
                    print(f"   ✅ Tablas encontradas: {len(tables)}")
                    for table in tables:
                        print(f"   - {table[0]}")
                        
                        # Contar registros en cada tabla
                        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                        count = cursor.fetchone()[0]
                        print(f"     Registros: {count}")
                else:
                    print("   ⚠️  No se encontraron tablas en la base de datos")
                    print("   💡 Necesitas importar el archivo crud_python.sql")
            else:
                print("   ❌ Base de datos 'crud_python' NO encontrada")
                print("   💡 Necesitas crear la base de datos primero")
                print("   📝 Revisa la GUIA_INICIO.md para instrucciones")
            
            cursor.close()
            connection.close()
            print("\n✅ Conexión cerrada correctamente")
            
        else:
            print("❌ No se pudo establecer la conexión")
            
    except mysql.connector.Error as error:
        print(f"\n❌ Error de conexión: {error}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que MySQL esté corriendo")
        print("   2. Revisa usuario y contraseña en conexionBD.py")
        print("   3. Asegúrate de que la base de datos existe")
        print("   4. Verifica que el puerto MySQL (3306) esté disponible")
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_conexion()


