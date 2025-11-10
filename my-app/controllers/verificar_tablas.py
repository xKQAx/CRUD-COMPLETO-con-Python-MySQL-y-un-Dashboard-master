"""
Función para verificar y crear las tablas de documentos y notificaciones si no existen
"""

from conexion.conexionBD import connectionBD

def verificar_y_crear_tablas_notificaciones():
    """
    Verifica si las tablas de documentos y notificaciones existen,
    y las crea si no existen.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Verificar si existe la tabla tbl_documentos
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE()
                    AND table_name = 'tbl_documentos'
                """)
                existe_documentos = cursor.fetchone()['count'] > 0
                
                # Verificar si existe la tabla tbl_notificaciones_config
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE()
                    AND table_name = 'tbl_notificaciones_config'
                """)
                existe_notificaciones = cursor.fetchone()['count'] > 0
                
                # Crear tabla tbl_documentos si no existe
                if not existe_documentos:
                    print("Creando tabla tbl_documentos...")
                    cursor.execute("""
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
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                    """)
                    print("Tabla tbl_documentos creada exitosamente")
                
                # Crear tabla tbl_notificaciones_config si no existe
                if not existe_notificaciones:
                    print("Creando tabla tbl_notificaciones_config...")
                    try:
                        # Crear tabla sin foreign key primero
                        cursor.execute("""
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
                              KEY `idx_notificado` (`notificado`)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                        """)
                        # Intentar agregar la foreign key si la tabla de documentos existe
                        if existe_documentos:
                            try:
                                # Verificar si la foreign key ya existe
                                cursor.execute("""
                                    SELECT COUNT(*) as count
                                    FROM information_schema.table_constraints 
                                    WHERE constraint_schema = DATABASE()
                                    AND table_name = 'tbl_notificaciones_config'
                                    AND constraint_name = 'fk_notificaciones_documento'
                                """)
                                fk_exists = cursor.fetchone()['count'] > 0
                                
                                if not fk_exists:
                                    cursor.execute("""
                                        ALTER TABLE `tbl_notificaciones_config`
                                        ADD CONSTRAINT `fk_notificaciones_documento` 
                                        FOREIGN KEY (`id_documento`) REFERENCES `tbl_documentos` (`id_documento`) ON DELETE CASCADE
                                    """)
                            except Exception as fk_error:
                                # Si la foreign key ya existe o hay un error, continuar
                                print(f"Advertencia al crear foreign key: {fk_error}")
                        print("Tabla tbl_notificaciones_config creada exitosamente")
                    except Exception as create_error:
                        print(f"Error al crear tabla tbl_notificaciones_config: {create_error}")
                        raise
                
                conexion_MySQLdb.commit()
                return True
    except Exception as e:
        print(f"Error al verificar/crear tablas: {e}")
        import traceback
        traceback.print_exc()
        return False

