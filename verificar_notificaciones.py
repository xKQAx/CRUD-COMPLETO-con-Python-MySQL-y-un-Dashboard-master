"""
Script para verificar y generar notificaciones de documentos próximos a vencer
Este script puede ejecutarse periódicamente mediante un cron job o tarea programada

Ejecutar manualmente:
    python verificar_notificaciones.py

O configurar en cron (Linux/Mac):
    0 9 * * * cd /ruta/al/proyecto && python verificar_notificaciones.py

O configurar en Task Scheduler (Windows):
    Crear una tarea programada que ejecute este script diariamente
"""

import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio my-app al path
base_dir = os.path.dirname(os.path.abspath(__file__))
my_app_path = os.path.join(base_dir, 'my-app')

if my_app_path not in sys.path:
    sys.path.insert(0, my_app_path)

# Cambiar al directorio my-app
os.chdir(my_app_path)

# Importar funciones de notificaciones
from controllers.funciones_documentos import verificar_y_generar_notificaciones

def main():
    print("=" * 60)
    print("VERIFICANDO NOTIFICACIONES DE DOCUMENTOS")
    print("=" * 60)
    
    try:
        cantidad = verificar_y_generar_notificaciones()
        print(f"\n✓ Verificación completada")
        print(f"  Notificaciones generadas: {cantidad}")
        print("=" * 60)
        return cantidad
    except Exception as e:
        print(f"\n✗ Error al verificar notificaciones: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        return 0

if __name__ == "__main__":
    main()

