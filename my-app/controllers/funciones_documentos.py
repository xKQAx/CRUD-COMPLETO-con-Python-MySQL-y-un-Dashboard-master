# Para subir archivo al servidor
from werkzeug.utils import secure_filename
import uuid
import os
from os import remove, path

# Importando conexión a BD
from conexion.conexionBD import connectionBD
import datetime


# Lista de Documentos
def sql_lista_documentosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        d.id_documento,
                        d.nombre_documento,
                        d.fecha_vencimiento,
                        d.descripcion,
                        d.archivo_documento,
                        DATE_FORMAT(d.fecha_registro, '%Y-%m-%d %h:%i %p') AS fecha_registro,
                        DATEDIFF(d.fecha_vencimiento, CURDATE()) AS dias_restantes
                    FROM tbl_documentos AS d
                    ORDER BY d.fecha_vencimiento ASC
                    """)
                cursor.execute(querySQL,)
                documentosBD = cursor.fetchall()
        return documentosBD if documentosBD else []
    except Exception as e:
        print(f"Error en la función sql_lista_documentosBD: {e}")
        return []


# Procesar archivo subido
def procesar_archivo_documento(archivo):
    try:
        if not archivo or archivo.filename == '':
            return None
            
        # Nombre original del archivo
        filename = secure_filename(archivo.filename)
        extension = os.path.splitext(filename)[1].lower()
        
        # Validar extensión (PDF o imágenes)
        extensiones_permitidas = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp']
        if extension not in extensiones_permitidas:
            raise ValueError(f"Extensión no permitida. Solo se permiten: {', '.join(extensiones_permitidas)}")
        
        # Crear un string único para el nombre del archivo
        nuevoNameFile = (uuid.uuid4().hex + uuid.uuid4().hex)[:100]
        nombreFile = nuevoNameFile + extension

        # Construir la ruta completa de subida del archivo
        basepath = os.path.abspath(os.path.dirname(__file__))
        upload_dir = os.path.join(basepath, f'../static/documentos/')

        # Validar si existe la ruta y crearla si no existe
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            # Dando permiso a la carpeta
            os.chmod(upload_dir, 0o755)

        # Construir la ruta completa de subida del archivo
        upload_path = os.path.join(upload_dir, nombreFile)
        archivo.save(upload_path)

        return nombreFile

    except Exception as e:
        print(f"Error al procesar archivo: {e}")
        return None


# Registrar nuevo documento
def procesar_form_documento(dataForm, archivo_documento=None):
    try:
        # Procesar archivo si existe
        nombre_archivo = None
        if archivo_documento and archivo_documento.filename != '':
            nombre_archivo = procesar_archivo_documento(archivo_documento)
            # Si se intentó subir un archivo pero falló, retornar None
            if nombre_archivo is None:
                return None
        
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """INSERT INTO tbl_documentos 
                         (nombre_documento, fecha_vencimiento, descripcion, archivo_documento) 
                         VALUES (%s, %s, %s, %s)"""

                # Creando una tupla con los valores del INSERT
                valores = (
                    dataForm['nombre_documento'],
                    dataForm['fecha_vencimiento'],
                    dataForm.get('descripcion', ''),
                    nombre_archivo
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                id_documento = cursor.lastrowid

                # Crear configuración de notificaciones por defecto
                crear_config_notificaciones(id_documento, dataForm)

                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        print(f"Error en procesar_form_documento: {e}")
        import traceback
        traceback.print_exc()
        return None


# Crear configuración de notificaciones por defecto
def crear_config_notificaciones(id_documento, dataForm):
    try:
        # Verificar y crear tablas si no existen
        from controllers.verificar_tablas import verificar_y_crear_tablas_notificaciones
        verificar_y_crear_tablas_notificaciones()
        
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Configuración para mismo día (0 días antes)
                sql_mismo_dia = """INSERT INTO tbl_notificaciones_config 
                                   (id_documento, dias_antes, notificar_mismo_dia, notificar_una_semana, notificar_un_mes) 
                                   VALUES (%s, 0, %s, 0, 0)"""
                # Verificar si viene como string '1' o como int 1, o si no existe usar '1' por defecto
                notificar_mismo_dia_val = dataForm.get('notificar_mismo_dia', '1')
                if notificar_mismo_dia_val is None or notificar_mismo_dia_val == '':
                    notificar_mismo_dia_val = '1'
                notificar_mismo_dia = 1 if str(notificar_mismo_dia_val) == '1' else 0
                cursor.execute(sql_mismo_dia, (id_documento, notificar_mismo_dia))

                # Configuración para una semana antes (7 días antes)
                sql_semana = """INSERT INTO tbl_notificaciones_config 
                                (id_documento, dias_antes, notificar_mismo_dia, notificar_una_semana, notificar_un_mes) 
                                VALUES (%s, 7, 0, %s, 0)"""
                notificar_semana_val = dataForm.get('notificar_una_semana', '1')
                if notificar_semana_val is None or notificar_semana_val == '':
                    notificar_semana_val = '1'
                notificar_semana = 1 if str(notificar_semana_val) == '1' else 0
                cursor.execute(sql_semana, (id_documento, notificar_semana))

                # Configuración para un mes antes (30 días antes)
                sql_mes = """INSERT INTO tbl_notificaciones_config 
                             (id_documento, dias_antes, notificar_mismo_dia, notificar_una_semana, notificar_un_mes) 
                             VALUES (%s, 30, 0, 0, %s)"""
                notificar_mes_val = dataForm.get('notificar_un_mes', '1')
                if notificar_mes_val is None or notificar_mes_val == '':
                    notificar_mes_val = '1'
                notificar_mes = 1 if str(notificar_mes_val) == '1' else 0
                cursor.execute(sql_mes, (id_documento, notificar_mes))

                conexion_MySQLdb.commit()
                return True
    except Exception as e:
        print(f"Error en crear_config_notificaciones: {e}")
        return False


# Detalles del Documento
def sql_detalles_documentoBD(idDocumento):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        d.id_documento,
                        d.nombre_documento,
                        d.fecha_vencimiento,
                        d.descripcion,
                        d.archivo_documento,
                        DATE_FORMAT(d.fecha_registro, '%Y-%m-%d %h:%i %p') AS fecha_registro,
                        DATE_FORMAT(d.fecha_actualizacion, '%Y-%m-%d %h:%i %p') AS fecha_actualizacion,
                        DATEDIFF(d.fecha_vencimiento, CURDATE()) AS dias_restantes
                    FROM tbl_documentos AS d
                    WHERE d.id_documento = %s
                    """)
                cursor.execute(querySQL, (idDocumento,))
                documentoBD = cursor.fetchone()
        return documentoBD
    except Exception as e:
        print(f"Error en la función sql_detalles_documentoBD: {e}")
        return None


# Buscar documento único
def buscarDocumentoUnico(id):
    try:
        # Verificar y crear tablas si no existen
        from controllers.verificar_tablas import verificar_y_crear_tablas_notificaciones
        verificar_y_crear_tablas_notificaciones()
        
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                    SELECT 
                        d.id_documento,
                        d.nombre_documento,
                        d.fecha_vencimiento,
                        d.descripcion,
                        d.archivo_documento
                    FROM tbl_documentos AS d
                    WHERE d.id_documento = %s LIMIT 1
                    """)
                mycursor.execute(querySQL, (id,))
                documento = mycursor.fetchone()
                
                # Debug: imprimir documento obtenido
                if documento:
                    print(f"Documento encontrado (ID {id}): {documento}")
                else:
                    print(f"Documento NO encontrado (ID {id})")
                
                return documento
    except Exception as e:
        print(f"Ocurrió un error en buscarDocumentoUnico: {e}")
        import traceback
        traceback.print_exc()
        return None


# Obtener configuración de notificaciones de un documento
def obtener_config_notificaciones(id_documento):
    try:
        # Verificar y crear tablas si no existen
        from controllers.verificar_tablas import verificar_y_crear_tablas_notificaciones
        verificar_y_crear_tablas_notificaciones()
        
        # Limpiar configuraciones duplicadas antes de obtenerlas
        from controllers.limpiar_notificaciones import limpiar_configuraciones_duplicadas
        limpiar_configuraciones_duplicadas(id_documento)
        
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        id_config,
                        id_documento,
                        dias_antes,
                        notificar_mismo_dia,
                        notificar_una_semana,
                        notificar_un_mes,
                        notificado,
                        fecha_notificacion
                    FROM tbl_notificaciones_config
                    WHERE id_documento = %s
                    ORDER BY dias_antes ASC
                    """)
                cursor.execute(querySQL, (id_documento,))
                configs = cursor.fetchall()
                
                # Debug: imprimir configuraciones obtenidas
                print(f"Configuraciones obtenidas para documento {id_documento}: {configs}")
                
                return configs
    except Exception as e:
        print(f"Error en obtener_config_notificaciones: {e}")
        import traceback
        traceback.print_exc()
        return []


# Actualizar documento
def procesar_actualizacion_documento(data):
    try:
        # Verificar y crear tablas si no existen
        from controllers.verificar_tablas import verificar_y_crear_tablas_notificaciones
        verificar_y_crear_tablas_notificaciones()
        
        # Procesar archivo si se subió uno nuevo
        nombre_archivo = None
        archivo_anterior = None
        
        # Obtener el archivo anterior si existe
        documento_actual = buscarDocumentoUnico(data.form['id_documento'])
        if documento_actual:
            archivo_anterior = documento_actual.get('archivo_documento')
        
        # Si se subió un archivo nuevo, procesarlo
        if 'archivo_documento' in data.files and data.files['archivo_documento'].filename != '':
            nombre_archivo = procesar_archivo_documento(data.files['archivo_documento'])
            if nombre_archivo is None:
                print("Error: No se pudo procesar el archivo")
                return None
            
            # Eliminar archivo anterior si existe
            if archivo_anterior:
                eliminar_archivo_documento(archivo_anterior)
        
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Extraer y procesar datos del formulario
                nombre_documento = data.form['nombre_documento']
                fecha_vencimiento = data.form['fecha_vencimiento']
                descripcion = data.form.get('descripcion', '')
                id_documento = data.form['id_documento']

                # Construir consulta SQL
                if nombre_archivo:
                    querySQL = """
                        UPDATE tbl_documentos
                        SET 
                            nombre_documento = %s,
                            fecha_vencimiento = %s,
                            descripcion = %s,
                            archivo_documento = %s
                        WHERE id_documento = %s
                    """
                    params = [
                        nombre_documento,
                        fecha_vencimiento,
                        descripcion,
                        nombre_archivo,
                        id_documento
                    ]
                else:
                    querySQL = """
                        UPDATE tbl_documentos
                        SET 
                            nombre_documento = %s,
                            fecha_vencimiento = %s,
                            descripcion = %s
                        WHERE id_documento = %s
                    """
                    params = [
                        nombre_documento,
                        fecha_vencimiento,
                        descripcion,
                        id_documento
                    ]

                cursor.execute(querySQL, params)
                conexion_MySQLdb.commit()
                
                resultado = cursor.rowcount
                
                # Siempre actualizar configuraciones de notificaciones, incluso si no hay cambios en el documento
                # Esto permite actualizar solo las configuraciones sin cambiar otros campos
                try:
                    # Limpiar configuraciones duplicadas primero
                    from controllers.limpiar_notificaciones import limpiar_configuraciones_duplicadas
                    limpiar_configuraciones_duplicadas(id_documento)
                    
                    # Actualizar configuraciones de notificaciones usando la misma conexión
                    # Eliminar configuraciones existentes
                    sql_delete = "DELETE FROM tbl_notificaciones_config WHERE id_documento = %s"
                    cursor.execute(sql_delete, (id_documento,))
                    print(f"Configuraciones eliminadas para documento {id_documento}")
                    
                    # Crear nuevas configuraciones
                    # Debug: imprimir todos los valores del formulario
                    print(f"Valores del formulario para documento {id_documento}:")
                    print(f"  notificar_mismo_dia: {data.form.get('notificar_mismo_dia')}")
                    print(f"  notificar_una_semana: {data.form.get('notificar_una_semana')}")
                    print(f"  notificar_un_mes: {data.form.get('notificar_un_mes')}")
                    print(f"  Todos los campos del form: {list(data.form.keys())}")
                    
                    # Configuración para mismo día (0 días antes)
                    sql_mismo_dia = """INSERT INTO tbl_notificaciones_config 
                                       (id_documento, dias_antes, notificar_mismo_dia, notificar_una_semana, notificar_un_mes) 
                                       VALUES (%s, 0, %s, 0, 0)"""
                    # Flask puede devolver una lista si hay múltiples valores con el mismo nombre
                    # Si hay lista, tomar el valor '1' si existe, sino '0'
                    notificar_mismo_dia_val = data.form.getlist('notificar_mismo_dia')
                    if not notificar_mismo_dia_val:
                        notificar_mismo_dia_val = ['0']
                    # Si hay '1' en la lista, el checkbox está marcado
                    notificar_mismo_dia = 1 if '1' in notificar_mismo_dia_val else 0
                    print(f"  Guardando notificar_mismo_dia = {notificar_mismo_dia} (valores: {notificar_mismo_dia_val})")
                    cursor.execute(sql_mismo_dia, (id_documento, notificar_mismo_dia))

                    # Configuración para una semana antes (7 días antes)
                    sql_semana = """INSERT INTO tbl_notificaciones_config 
                                    (id_documento, dias_antes, notificar_mismo_dia, notificar_una_semana, notificar_un_mes) 
                                    VALUES (%s, 7, 0, %s, 0)"""
                    notificar_semana_val = data.form.getlist('notificar_una_semana')
                    if not notificar_semana_val:
                        notificar_semana_val = ['0']
                    notificar_semana = 1 if '1' in notificar_semana_val else 0
                    print(f"  Guardando notificar_una_semana = {notificar_semana} (valores: {notificar_semana_val})")
                    cursor.execute(sql_semana, (id_documento, notificar_semana))

                    # Configuración para un mes antes (30 días antes)
                    sql_mes = """INSERT INTO tbl_notificaciones_config 
                                 (id_documento, dias_antes, notificar_mismo_dia, notificar_una_semana, notificar_un_mes) 
                                 VALUES (%s, 30, 0, 0, %s)"""
                    notificar_mes_val = data.form.getlist('notificar_un_mes')
                    if not notificar_mes_val:
                        notificar_mes_val = ['0']
                    notificar_mes = 1 if '1' in notificar_mes_val else 0
                    print(f"  Guardando notificar_un_mes = {notificar_mes} (valores: {notificar_mes_val})")
                    cursor.execute(sql_mes, (id_documento, notificar_mes))
                    
                    conexion_MySQLdb.commit()
                    print(f"Configuraciones de notificaciones actualizadas exitosamente para documento {id_documento}")
                except Exception as e:
                    print(f"Advertencia: Error al actualizar configuraciones de notificaciones: {e}")
                    import traceback
                    traceback.print_exc()
                    # Hacer rollback si hay error en las configuraciones
                    conexion_MySQLdb.rollback()
                    # Pero no retornar None porque el documento puede haberse actualizado

                # Retornar éxito si se actualizó el documento O si se actualizaron las configuraciones
                # Si no hay cambios en el documento pero sí en las configuraciones, retornar 1 para indicar éxito
                if resultado > 0:
                    return resultado
                else:
                    # Si no hubo cambios en el documento, pero se actualizaron las configuraciones, retornar 1
                    # Esto permite que el botón funcione incluso sin cambios en los campos principales
                    return 1
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_documento: {e}")
        import traceback
        traceback.print_exc()
        return None


# Actualizar configuración de notificaciones
def actualizar_config_notificaciones(id_documento, dataForm):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Eliminar configuraciones existentes
                sql_delete = "DELETE FROM tbl_notificaciones_config WHERE id_documento = %s"
                cursor.execute(sql_delete, (id_documento,))

                # Crear nuevas configuraciones directamente aquí para usar la misma conexión
                # Configuración para mismo día (0 días antes)
                sql_mismo_dia = """INSERT INTO tbl_notificaciones_config 
                                   (id_documento, dias_antes, notificar_mismo_dia, notificar_una_semana, notificar_un_mes) 
                                   VALUES (%s, 0, %s, 0, 0)"""
                notificar_mismo_dia_val = dataForm.get('notificar_mismo_dia', '0')
                # Si el checkbox está marcado, viene como '1', si no, viene el hidden como '0'
                # Si viene '1' del checkbox, ese es el valor; si viene '0' del hidden, también es válido
                notificar_mismo_dia = 1 if str(notificar_mismo_dia_val) == '1' else 0
                cursor.execute(sql_mismo_dia, (id_documento, notificar_mismo_dia))

                # Configuración para una semana antes (7 días antes)
                sql_semana = """INSERT INTO tbl_notificaciones_config 
                                (id_documento, dias_antes, notificar_mismo_dia, notificar_una_semana, notificar_un_mes) 
                                VALUES (%s, 7, 0, %s, 0)"""
                notificar_semana_val = dataForm.get('notificar_una_semana', '0')
                notificar_semana = 1 if str(notificar_semana_val) == '1' else 0
                cursor.execute(sql_semana, (id_documento, notificar_semana))

                # Configuración para un mes antes (30 días antes)
                sql_mes = """INSERT INTO tbl_notificaciones_config 
                             (id_documento, dias_antes, notificar_mismo_dia, notificar_una_semana, notificar_un_mes) 
                             VALUES (%s, 30, 0, 0, %s)"""
                notificar_mes_val = dataForm.get('notificar_un_mes', '0')
                notificar_mes = 1 if str(notificar_mes_val) == '1' else 0
                cursor.execute(sql_mes, (id_documento, notificar_mes))

                conexion_MySQLdb.commit()
                return True
    except Exception as e:
        print(f"Error en actualizar_config_notificaciones: {e}")
        import traceback
        traceback.print_exc()
        return False


# Eliminar archivo físico del servidor
def eliminar_archivo_documento(nombre_archivo):
    try:
        if nombre_archivo:
            basepath = path.dirname(__file__)
            url_file = path.join(basepath, '../static/documentos', nombre_archivo)
            
            if path.exists(url_file):
                remove(url_file)
                return True
        return False
    except Exception as e:
        print(f"Error al eliminar archivo: {e}")
        return False


# Eliminar documento
def eliminarDocumento(id_documento):
    try:
        # Obtener el nombre del archivo antes de eliminar
        documento = buscarDocumentoUnico(id_documento)
        archivo_documento = documento.get('archivo_documento') if documento else None
        
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Las notificaciones se eliminan automáticamente por CASCADE
                querySQL = "DELETE FROM tbl_documentos WHERE id_documento = %s"
                cursor.execute(querySQL, (id_documento,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount
                
                # Eliminar archivo físico si existe
                if resultado_eliminar and archivo_documento:
                    eliminar_archivo_documento(archivo_documento)

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarDocumento: {e}")
        return None


# Buscar documentos por término
def buscarDocumentoBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                    SELECT 
                        d.id_documento,
                        d.nombre_documento,
                        d.fecha_vencimiento,
                        DATEDIFF(d.fecha_vencimiento, CURDATE()) AS dias_restantes
                    FROM tbl_documentos AS d
                    WHERE d.nombre_documento LIKE %s OR d.descripcion LIKE %s
                    ORDER BY d.fecha_vencimiento ASC
                    """)
                search_pattern = f"%{search}%"
                mycursor.execute(querySQL, (search_pattern, search_pattern))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda if resultado_busqueda else []
    except Exception as e:
        print(f"Ocurrió un error en buscarDocumentoBD: {e}")
        return []


# Obtener documentos próximos a vencer (para notificaciones)
def obtener_documentos_proximos_vencer(dias=30):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        d.id_documento,
                        d.nombre_documento,
                        d.fecha_vencimiento,
                        DATEDIFF(d.fecha_vencimiento, CURDATE()) AS dias_restantes,
                        nc.id_config,
                        nc.dias_antes,
                        nc.notificado
                    FROM tbl_documentos AS d
                    INNER JOIN tbl_notificaciones_config AS nc ON d.id_documento = nc.id_documento
                    WHERE DATEDIFF(d.fecha_vencimiento, CURDATE()) <= %s
                    AND DATEDIFF(d.fecha_vencimiento, CURDATE()) >= 0
                    AND nc.notificado = 0
                    AND (
                        (nc.dias_antes = 0 AND nc.notificar_mismo_dia = 1) OR
                        (nc.dias_antes = 7 AND nc.notificar_una_semana = 1) OR
                        (nc.dias_antes = 30 AND nc.notificar_un_mes = 1)
                    )
                    ORDER BY d.fecha_vencimiento ASC
                    """)
                cursor.execute(querySQL, (dias,))
                documentos = cursor.fetchall()
        return documentos
    except Exception as e:
        print(f"Error en obtener_documentos_proximos_vencer: {e}")
        return []


# Obtener notificaciones pendientes (agrupadas por documento)
def obtener_notificaciones_pendientes():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener todos los documentos con sus configuraciones
                querySQL = ("""
                    SELECT 
                        d.id_documento,
                        d.nombre_documento,
                        d.fecha_vencimiento,
                        DATEDIFF(d.fecha_vencimiento, CURDATE()) AS dias_restantes,
                        nc.dias_antes,
                        nc.notificar_mismo_dia,
                        nc.notificar_una_semana,
                        nc.notificar_un_mes,
                        nc.notificado
                    FROM tbl_documentos AS d
                    INNER JOIN tbl_notificaciones_config AS nc ON d.id_documento = nc.id_documento
                    WHERE DATEDIFF(d.fecha_vencimiento, CURDATE()) <= 30
                    AND nc.notificado = 0
                    ORDER BY d.fecha_vencimiento ASC, nc.dias_antes ASC
                    """)
                cursor.execute(querySQL)
                resultados = cursor.fetchall()
                
                # Procesar y agrupar por documento
                documentos_dict = {}
                for row in resultados:
                    id_doc = row['id_documento']
                    dias_restantes = row['dias_restantes']
                    dias_antes = row['dias_antes']
                    
                    # Verificar si debe mostrar notificación según la configuración
                    debe_mostrar = False
                    
                    if dias_antes == 0 and row['notificar_mismo_dia'] == 1:
                        # Notificar el mismo día (días restantes = 0 o negativo)
                        if dias_restantes <= 0:
                            debe_mostrar = True
                    elif dias_antes == 7 and row['notificar_una_semana'] == 1:
                        # Notificar una semana antes (exactamente cuando faltan 7 días o menos, pero más de 0)
                        if 0 < dias_restantes <= 7:
                            debe_mostrar = True
                    elif dias_antes == 30 and row['notificar_un_mes'] == 1:
                        # Notificar un mes antes (exactamente cuando faltan 30 días o menos, pero más de 7)
                        # Si está configurado para 30 días, mostrar cuando falten entre 8 y 30 días
                        if 7 < dias_restantes <= 30:
                            debe_mostrar = True
                    
                    if debe_mostrar:
                        if id_doc not in documentos_dict:
                            documentos_dict[id_doc] = {
                                'id_documento': id_doc,
                                'nombre_documento': row['nombre_documento'],
                                'fecha_vencimiento': row['fecha_vencimiento'],
                                'dias_restantes': dias_restantes,
                                'dias_antes_list': []
                            }
                        if dias_antes not in documentos_dict[id_doc]['dias_antes_list']:
                            documentos_dict[id_doc]['dias_antes_list'].append(dias_antes)
                
                # Convertir a lista y generar mensajes
                notificaciones = []
                for doc in documentos_dict.values():
                    # Determinar el mensaje de notificación basado en el día más cercano
                    dias_list = sorted(doc['dias_antes_list'])
                    dias_restantes = doc['dias_restantes']
                    
                    if dias_restantes < 0:
                        doc['mensaje'] = f"El documento '{doc['nombre_documento']}' está VENCIDO ({abs(dias_restantes)} días)"
                        doc['tipo'] = 'vencido'
                    elif dias_restantes == 0:
                        doc['mensaje'] = f"El documento '{doc['nombre_documento']}' vence HOY"
                        doc['tipo'] = 'urgente'
                    elif dias_restantes <= 7:
                        doc['mensaje'] = f"El documento '{doc['nombre_documento']}' vence en {dias_restantes} días"
                        doc['tipo'] = 'advertencia'
                    elif dias_restantes <= 30:
                        doc['mensaje'] = f"El documento '{doc['nombre_documento']}' vence en {dias_restantes} días"
                        doc['tipo'] = 'info'
                    else:
                        doc['mensaje'] = f"El documento '{doc['nombre_documento']}' vence en {dias_restantes} días"
                        doc['tipo'] = 'info'
                    
                    notificaciones.append(doc)
                
        return notificaciones
    except Exception as e:
        print(f"Error en obtener_notificaciones_pendientes: {e}")
        import traceback
        traceback.print_exc()
        return []


# Marcar notificación como enviada
def marcar_notificacion_enviada(id_documento, dias_antes):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    UPDATE tbl_notificaciones_config
                    SET notificado = 1,
                        fecha_notificacion = NOW()
                    WHERE id_documento = %s
                    AND dias_antes = %s
                    AND notificado = 0
                    """)
                cursor.execute(querySQL, (id_documento, dias_antes))
                conexion_MySQLdb.commit()
                return cursor.rowcount > 0
    except Exception as e:
        print(f"Error en marcar_notificacion_enviada: {e}")
        return False


# Marcar todas las notificaciones de un documento como leídas
def marcar_todas_notificaciones_leidas(id_documento):
    """
    Marca todas las notificaciones pendientes de un documento como leídas
    Útil cuando el usuario revisa el documento
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    UPDATE tbl_notificaciones_config
                    SET notificado = 1,
                        fecha_notificacion = NOW()
                    WHERE id_documento = %s
                    AND notificado = 0
                    """)
                cursor.execute(querySQL, (id_documento,))
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error en marcar_todas_notificaciones_leidas: {e}")
        return 0


# Verificar y generar notificaciones automáticamente
def verificar_y_generar_notificaciones():
    """
    Verifica documentos próximos a vencer y genera notificaciones
    Retorna el número de notificaciones generadas
    """
    try:
        documentos = obtener_documentos_proximos_vencer(30)
        notificaciones_generadas = 0
        
        for documento in documentos:
            dias_restantes = documento['dias_restantes']
            dias_antes = documento['dias_antes']
            
            # Verificar si debe notificarse según los días restantes
            debe_notificar = False
            if dias_antes == 0 and dias_restantes <= 0:
                # Notificar el mismo día o si ya venció
                debe_notificar = True
            elif dias_antes == 7 and 0 < dias_restantes <= 7:
                # Notificar cuando falten entre 1 y 7 días
                debe_notificar = True
            elif dias_antes == 30 and 7 < dias_restantes <= 30:
                # Notificar cuando falten entre 8 y 30 días
                debe_notificar = True
            
            if debe_notificar:
                # Marcar como notificado
                if marcar_notificacion_enviada(documento['id_documento'], dias_antes):
                    notificaciones_generadas += 1
        
        return notificaciones_generadas
    except Exception as e:
        print(f"Error en verificar_y_generar_notificaciones: {e}")
        import traceback
        traceback.print_exc()
        return 0

