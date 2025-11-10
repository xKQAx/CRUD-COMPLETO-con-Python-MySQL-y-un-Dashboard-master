"""
Script para crear las tablas de documentos y notificaciones
Ejecuta este script si ya tienes la base de datos creada y quieres agregar las nuevas tablas
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

def crear_tablas_documentos():
    print("=" * 60)
    print(f"CREANDO TABLAS DE DOCUMENTOS EN {MYSQL_DATABASE}")
    print("=" * 60)
    
    try:
        # Conectar a MySQL
        print("\n1. Conectando a MySQL...")
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        
        if connection.is_connected():
            print("   Conexión exitosa a MySQL")
            
            cursor = connection.cursor()
            
            # Crear tabla tbl_documentos
            print("\n2. Creando tabla tbl_documentos...")
            sql_documentos = """
            CREATE TABLE IF NOT EXISTS `tbl_documentos` (
              `id_documento` int NOT NULL AUTO_INCREMENT,
              `nombre_documento` varchar(100) NOT NULL,
              `fecha_vencimiento` date NOT NULL,
              `descripcion` text,
              `archivo_documento` mediumtext COMMENT 'Nombre del archivo PDF o imagen',
              `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
              `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (`id_documento`),
              KEY `idx_fecha_vencimiento` (`fecha_vencimiento`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """
            cursor.execute(sql_documentos)
            print("   Tabla tbl_documentos creada exitosamente")
            
            # Crear tabla tbl_notificaciones_config
            print("\n3. Creando tabla tbl_notificaciones_config...")
            sql_notificaciones = """
            CREATE TABLE IF NOT EXISTS `tbl_notificaciones_config` (
              `id_config` int NOT NULL AUTO_INCREMENT,
              `id_documento` int NOT NULL,
              `dias_antes` int NOT NULL COMMENT 'Días antes del vencimiento para notificar (0=mismo día, 7=una semana, 30=un mes)',
              `notificar_mismo_dia` tinyint(1) DEFAULT 1 COMMENT '1=Notificar el mismo día, 0=No notificar',
              `notificar_una_semana` tinyint(1) DEFAULT 1 COMMENT '1=Notificar una semana antes, 0=No notificar',
              `notificar_un_mes` tinyint(1) DEFAULT 1 COMMENT '1=Notificar un mes antes, 0=No notificar',
              `notificado` tinyint(1) DEFAULT 0 COMMENT '0=No notificado, 1=Ya notificado',
              `fecha_notificacion` timestamp NULL DEFAULT NULL,
              `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id_config`),
              KEY `idx_id_documento` (`id_documento`),
              KEY `idx_notificado` (`notificado`),
              CONSTRAINT `fk_notificaciones_documento` FOREIGN KEY (`id_documento`) REFERENCES `tbl_documentos` (`id_documento`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """
            cursor.execute(sql_notificaciones)
            print("   Tabla tbl_notificaciones_config creada exitosamente")
            
            connection.commit()
            
            # Verificar tablas
            print("\n4. Verificando tablas creadas...")
            cursor.execute("SHOW TABLES LIKE 'tbl_documentos'")
            if cursor.fetchone():
                print("   [OK] tbl_documentos existe")
            else:
                print("   [ERROR] tbl_documentos NO existe")
            
            cursor.execute("SHOW TABLES LIKE 'tbl_notificaciones_config'")
            if cursor.fetchone():
                print("   [OK] tbl_notificaciones_config existe")
            else:
                print("   [ERROR] tbl_notificaciones_config NO existe")
            
            cursor.close()
            connection.close()
            
            print("\n" + "=" * 60)
            print("Tablas creadas exitosamente")
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
        print(f"  3. Asegúrate de que la base de datos '{MYSQL_DATABASE}' exista")
        return False
        
    except Exception as e:
        print(f"\nError inesperado: {e}")
        return False

if __name__ == "__main__":
    crear_tablas_documentos()

