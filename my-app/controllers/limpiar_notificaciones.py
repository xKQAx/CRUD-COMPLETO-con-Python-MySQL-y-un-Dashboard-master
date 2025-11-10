"""
Función para limpiar datos duplicados o incorrectos en la tabla de notificaciones
"""

from conexion.conexionBD import connectionBD

def limpiar_configuraciones_duplicadas(id_documento=None):
    """
    Limpia configuraciones duplicadas o incorrectas en la tabla de notificaciones.
    Si se proporciona id_documento, solo limpia ese documento.
    Si no se proporciona, limpia todos los documentos.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                if id_documento:
                    # Limpiar solo para un documento específico
                    # Eliminar duplicados, manteniendo solo el más reciente de cada dias_antes
                    cursor.execute("""
                        DELETE nc1 FROM tbl_notificaciones_config nc1
                        INNER JOIN tbl_notificaciones_config nc2 
                        WHERE nc1.id_documento = %s
                        AND nc1.id_documento = nc2.id_documento
                        AND nc1.dias_antes = nc2.dias_antes
                        AND nc1.id_config < nc2.id_config
                    """, (id_documento,))
                    
                    # Asegurar que solo haya una configuración por cada dias_antes (0, 7, 30)
                    # Eliminar configuraciones con dias_antes que no sean 0, 7 o 30
                    cursor.execute("""
                        DELETE FROM tbl_notificaciones_config
                        WHERE id_documento = %s
                        AND dias_antes NOT IN (0, 7, 30)
                    """, (id_documento,))
                    
                    # Verificar que solo haya una configuración por cada dias_antes
                    cursor.execute("""
                        SELECT dias_antes, COUNT(*) as count
                        FROM tbl_notificaciones_config
                        WHERE id_documento = %s
                        GROUP BY dias_antes
                        HAVING count > 1
                    """, (id_documento,))
                    
                    duplicados = cursor.fetchall()
                    for dup in duplicados:
                        # Obtener el ID más reciente para mantenerlo
                        cursor.execute("""
                            SELECT MAX(id_config) as max_id
                            FROM tbl_notificaciones_config
                            WHERE id_documento = %s
                            AND dias_antes = %s
                        """, (id_documento, dup['dias_antes']))
                        max_id = cursor.fetchone()['max_id']
                        
                        # Eliminar todos excepto el más reciente
                        cursor.execute("""
                            DELETE FROM tbl_notificaciones_config
                            WHERE id_documento = %s
                            AND dias_antes = %s
                            AND id_config != %s
                        """, (id_documento, dup['dias_antes'], max_id))
                    
                    conexion_MySQLdb.commit()
                    return True
                else:
                    # Limpiar para todos los documentos
                    # Eliminar duplicados
                    cursor.execute("""
                        DELETE nc1 FROM tbl_notificaciones_config nc1
                        INNER JOIN tbl_notificaciones_config nc2 
                        WHERE nc1.id_documento = nc2.id_documento
                        AND nc1.dias_antes = nc2.dias_antes
                        AND nc1.id_config < nc2.id_config
                    """)
                    
                    # Eliminar configuraciones con dias_antes inválidos
                    cursor.execute("""
                        DELETE FROM tbl_notificaciones_config
                        WHERE dias_antes NOT IN (0, 7, 30)
                    """)
                    
                    conexion_MySQLdb.commit()
                    return True
    except Exception as e:
        print(f"Error al limpiar configuraciones: {e}")
        import traceback
        traceback.print_exc()
        return False

