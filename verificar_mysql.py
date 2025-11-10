"""
Script para verificar el estado de MySQL y proporcionar instrucciones
"""
import subprocess
import sys
import os

def verificar_servicio_mysql():
    """Verifica si el servicio MySQL está instalado y corriendo"""
    print("=" * 60)
    print("VERIFICACIÓN DE MYSQL")
    print("=" * 60)
    
    try:
        # Intentar obtener servicios de MySQL usando PowerShell
        cmd = ['powershell', '-Command', 
               'Get-Service | Where-Object {$_.Name -like "*mysql*" -or $_.DisplayName -like "*mysql*"} | Select-Object Name, Status, DisplayName | Format-Table -AutoSize']
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if result.stdout.strip():
            print("\n[OK] Servicios MySQL encontrados:")
            print(result.stdout)
        else:
            print("\n[ERROR] No se encontraron servicios MySQL instalados")
            print("\n[INFO] Necesitas instalar MySQL primero.")
            print("   Revisa el archivo INSTRUCCIONES_MYSQL.md para mas detalles")
            return False
            
    except Exception as e:
        print(f"\n[ADVERTENCIA] Error al verificar servicios: {e}")
        print("\n💡 Intenta verificar manualmente:")
        print("   1. Abre el Administrador de servicios de Windows")
        print("   2. Busca servicios que contengan 'MySQL' en el nombre")
        return False
    
    # Intentar conectar a MySQL
    print("\n" + "=" * 60)
    print("PRUEBA DE CONEXIÓN A MYSQL")
    print("=" * 60)
    
    try:
        # Agregar my-app al path
        my_app_path = os.path.join(os.path.dirname(__file__), 'my-app')
        if my_app_path not in sys.path:
            sys.path.insert(0, my_app_path)
        
        from conexion.conexionBD import connectionBD
        
        print("\n1. Intentando conectar a MySQL...")
        connection = connectionBD()
        
        if connection and connection.is_connected():
            print("   [OK] Conexion exitosa!")
            
            # Obtener información
            db_info = connection.get_server_info()
            print(f"   - Version del servidor MySQL: {db_info}")
            
            cursor = connection.cursor()
            
            # Verificar base de datos
            print("\n2. Verificando base de datos 'crud_python'...")
            cursor.execute("SHOW DATABASES LIKE 'crud_python'")
            result = cursor.fetchone()
            
            if result:
                print("   [OK] Base de datos 'crud_python' encontrada")
                
                # Verificar tablas
                cursor.execute("USE crud_python")
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                if tables:
                    print(f"   [OK] Tablas encontradas: {len(tables)}")
                else:
                    print("   [ADVERTENCIA] No se encontraron tablas")
                    print("   [INFO] Ejecuta: python crear_bd.py")
            else:
                print("   [ERROR] Base de datos 'crud_python' NO encontrada")
                print("   [INFO] Ejecuta: python crear_bd.py")
            
            cursor.close()
            connection.close()
            print("\n[OK] Todo esta configurado correctamente")
            return True
        else:
            print("   [ERROR] No se pudo establecer la conexion")
            print("\n[INFO] Posibles soluciones:")
            print("   1. Verifica que MySQL este corriendo")
            print("   2. Revisa usuario y contrasena en my-app/conexion/conexionBD.py")
            print("   3. Asegurate de que el puerto 3306 este disponible")
            return False
            
    except ImportError as e:
        print(f"   [ERROR] Error al importar modulos: {e}")
        return False
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        print("\n[INFO] Posibles soluciones:")
        print("   1. Verifica que MySQL este instalado y corriendo")
        print("   2. Revisa las credenciales en my-app/conexion/conexionBD.py")
        print("   3. Asegurate de que la base de datos exista (ejecuta: python crear_bd.py)")
        return False

def mostrar_instrucciones_inicio():
    """Muestra instrucciones para iniciar MySQL"""
    print("\n" + "=" * 60)
    print("INSTRUCCIONES PARA INICIAR MYSQL")
    print("=" * 60)
    print("\nOpcion 1: Desde el Administrador de Servicios")
    print("   1. Presiona Win + R")
    print("   2. Escribe: services.msc")
    print("   3. Busca el servicio 'MySQL' o 'MySQL80'")
    print("   4. Haz clic derecho -> Iniciar")
    
    print("\nOpción 2: Desde PowerShell (como Administrador)")
    print("   Start-Service MySQL80")
    print("   # O el nombre que tenga tu servicio MySQL")
    
    print("\nOpción 3: Si usas XAMPP")
    print("   1. Abre el Panel de Control de XAMPP")
    print("   2. Haz clic en 'Start' junto a MySQL")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    mysql_ok = verificar_servicio_mysql()
    
    if not mysql_ok:
        mostrar_instrucciones_inicio()
        print("\n[INFO] Revisa el archivo INSTRUCCIONES_MYSQL.md para mas detalles")
    else:
        print("\n[OK] Puedes ejecutar la aplicacion con: python run.py")

