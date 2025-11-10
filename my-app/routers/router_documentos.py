from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify, send_from_directory
import os

# Importando conexión a BD
from controllers.funciones_documentos import *

PATH_URL = "public/documentos"


@app.route('/registrar-documento', methods=['GET'])
def viewFormDocumento():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_documento.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-documento', methods=['POST'])
def formDocumento():
    if 'conectado' in session:
        archivo_documento = None
        if 'archivo_documento' in request.files:
            archivo_documento = request.files['archivo_documento']
        
        resultado = procesar_form_documento(request.form, archivo_documento)
        if resultado:
            flash('El documento fue registrado correctamente', 'success')
            return redirect(url_for('lista_documentos'))
        else:
            flash('El documento NO fue registrado.', 'error')
            return render_template(f'{PATH_URL}/form_documento.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-documentos', methods=['GET'])
def lista_documentos():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_documentos.html', documentos=sql_lista_documentosBD())
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-documento/", methods=['GET'])
@app.route("/detalles-documento/<int:idDocumento>", methods=['GET'])
def detalleDocumento(idDocumento=None):
    if 'conectado' in session:
        if idDocumento is None:
            return redirect(url_for('inicio'))
        else:
            # Marcar todas las notificaciones de este documento como leídas cuando se visualiza
            from controllers.funciones_documentos import marcar_todas_notificaciones_leidas
            marcar_todas_notificaciones_leidas(idDocumento)
            
            detalle_documento = sql_detalles_documentoBD(idDocumento) or []
            config_notificaciones = obtener_config_notificaciones(idDocumento)
            return render_template(
                f'{PATH_URL}/detalles_documento.html',
                detalle_documento=detalle_documento,
                config_notificaciones=config_notificaciones
            )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Búsqueda de documentos
@app.route("/buscando-documento", methods=['POST'])
def viewBuscarDocumentoBD():
    resultadoBusqueda = buscarDocumentoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_documento.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-documento/<int:id>", methods=['GET'])
def viewEditarDocumento(id):
    if 'conectado' in session:
        respuestaDocumento = buscarDocumentoUnico(id)
        if respuestaDocumento:
            # Debug: imprimir documento obtenido
            print(f"Documento obtenido para edición (ID {id}): {respuestaDocumento}")
            
            config_notificaciones = obtener_config_notificaciones(id)
            # Debug: imprimir configuraciones obtenidas
            print(f"Configuraciones obtenidas para documento {id}: {config_notificaciones}")
            
            # Convertir configuraciones a formato más fácil de usar
            config_dict = {
                'notificar_mismo_dia': 0,
                'notificar_una_semana': 0,
                'notificar_un_mes': 0
            }
            
            # Si hay configuraciones, usarlas; si no, usar valores por defecto
            if config_notificaciones and len(config_notificaciones) > 0:
                for config in config_notificaciones:
                    dias_antes = int(config.get('dias_antes', -1))
                    print(f"Procesando configuración: dias_antes={dias_antes}, config={config}")
                    
                    if dias_antes == 0:
                        # Para mismo día (dias_antes=0), el valor está en notificar_mismo_dia
                        valor = int(config.get('notificar_mismo_dia', 0))
                        config_dict['notificar_mismo_dia'] = valor
                        print(f"  -> notificar_mismo_dia = {valor}")
                    elif dias_antes == 7:
                        # Para una semana (dias_antes=7), el valor está en notificar_una_semana
                        valor = int(config.get('notificar_una_semana', 0))
                        config_dict['notificar_una_semana'] = valor
                        print(f"  -> notificar_una_semana = {valor}")
                    elif dias_antes == 30:
                        # Para un mes (dias_antes=30), el valor está en notificar_un_mes
                        valor = int(config.get('notificar_un_mes', 0))
                        config_dict['notificar_un_mes'] = valor
                        print(f"  -> notificar_un_mes = {valor}")
            else:
                # Si no hay configuraciones, usar valores por defecto (todos activos)
                config_dict = {
                    'notificar_mismo_dia': 1,
                    'notificar_una_semana': 1,
                    'notificar_un_mes': 1
                }
            
            # Debug: imprimir config_dict final
            print(f"Config_dict final para documento {id}: {config_dict}")
            
            respuestaDocumento['config_notificaciones'] = config_dict
            return render_template(f'{PATH_URL}/form_documento_update.html', respuestaDocumento=respuestaDocumento)
        else:
            flash('El documento no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actualizar información de documento
@app.route('/actualizar-documento', methods=['POST'])
def actualizarDocumento():
    if 'conectado' in session:
        try:
            resultData = procesar_actualizacion_documento(request)
            if resultData and resultData > 0:
                flash('El documento fue actualizado correctamente', 'success')
                return redirect(url_for('lista_documentos'))
            else:
                flash('Error al actualizar el documento. Verifica los datos ingresados.', 'error')
                # Redirigir al formulario de edición para que el usuario pueda corregir
                id_documento = request.form.get('id_documento')
                if id_documento:
                    return redirect(url_for('viewEditarDocumento', id=id_documento))
                else:
                    return redirect(url_for('lista_documentos'))
        except Exception as e:
            print(f"Error en actualizarDocumento: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Error al actualizar el documento: {str(e)}', 'error')
            id_documento = request.form.get('id_documento')
            if id_documento:
                return redirect(url_for('viewEditarDocumento', id=id_documento))
            else:
                return redirect(url_for('lista_documentos'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/borrar-documento/<string:id_documento>', methods=['GET'])
def borrarDocumento(id_documento):
    if 'conectado' in session:
        resp = eliminarDocumento(id_documento)
        if resp:
            flash('El documento fue eliminado correctamente', 'success')
            return redirect(url_for('lista_documentos'))
        else:
            flash('Error al eliminar el documento.', 'error')
            return redirect(url_for('lista_documentos'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para descargar archivos de documentos
@app.route('/descargar-documento/<string:nombre_archivo>', methods=['GET'])
def descargar_documento(nombre_archivo):
    if 'conectado' in session:
        try:
            # Obtener la ruta del directorio de documentos
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            documentos_dir = os.path.join(base_dir, 'static', 'documentos')
            
            # Verificar que el archivo existe
            archivo_path = os.path.join(documentos_dir, nombre_archivo)
            if os.path.exists(archivo_path):
                return send_from_directory(
                    documentos_dir,
                    nombre_archivo,
                    as_attachment=True
                )
            else:
                flash('El archivo no existe.', 'error')
                return redirect(url_for('lista_documentos'))
        except Exception as e:
            print(f"Error al descargar archivo: {e}")
            flash('Error al descargar el archivo.', 'error')
            return redirect(url_for('lista_documentos'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para obtener notificaciones pendientes (API)
@app.route('/api/notificaciones-pendientes', methods=['GET'])
def api_notificaciones_pendientes():
    if 'conectado' in session:
        notificaciones = obtener_notificaciones_pendientes()
        return jsonify({
            'notificaciones': notificaciones,
            'total': len(notificaciones)
        })
    else:
        return jsonify({'error': 'No autorizado'}), 401


# Ruta para marcar notificación como leída
@app.route('/api/marcar-notificacion-leida', methods=['POST'])
def api_marcar_notificacion_leida():
    if 'conectado' in session:
        try:
            data = request.json
            id_documento = data.get('id_documento')
            dias_antes = data.get('dias_antes')
            
            if id_documento and dias_antes is not None:
                resultado = marcar_notificacion_enviada(id_documento, dias_antes)
                if resultado:
                    return jsonify({'success': True, 'message': 'Notificación marcada como leída'})
                else:
                    return jsonify({'success': False, 'message': 'Error al marcar notificación'}), 400
            else:
                return jsonify({'success': False, 'message': 'Datos incompletos'}), 400
        except Exception as e:
            print(f"Error en api_marcar_notificacion_leida: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401


# Ruta para marcar todas las notificaciones de un documento como leídas
@app.route('/api/marcar-todas-notificaciones-leidas', methods=['POST'])
def api_marcar_todas_notificaciones_leidas():
    if 'conectado' in session:
        try:
            data = request.json
            id_documento = data.get('id_documento')
            
            if id_documento:
                from controllers.funciones_documentos import marcar_todas_notificaciones_leidas
                cantidad = marcar_todas_notificaciones_leidas(id_documento)
                return jsonify({
                    'success': True,
                    'message': f'Se marcaron {cantidad} notificaciones como leídas',
                    'cantidad': cantidad
                })
            else:
                return jsonify({'success': False, 'message': 'ID de documento requerido'}), 400
        except Exception as e:
            print(f"Error en api_marcar_todas_notificaciones_leidas: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401


# Ruta para verificar y generar notificaciones (puede llamarse manualmente o por cron)
@app.route('/api/verificar-notificaciones', methods=['POST'])
def api_verificar_notificaciones():
    if 'conectado' in session:
        try:
            cantidad = verificar_y_generar_notificaciones()
            return jsonify({
                'success': True,
                'message': f'Se generaron {cantidad} notificaciones',
                'cantidad': cantidad
            })
        except Exception as e:
            print(f"Error en api_verificar_notificaciones: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'error': 'No autorizado'}), 401


# Ruta para obtener documentos próximos a vencer (API para notificaciones)
@app.route('/api/documentos-proximos-vencer', methods=['GET'])
def api_documentos_proximos_vencer():
    if 'conectado' in session:
        dias = request.args.get('dias', 30, type=int)
        documentos = obtener_documentos_proximos_vencer(dias)
        return jsonify(documentos)
    else:
        return jsonify({'error': 'No autorizado'}), 401

