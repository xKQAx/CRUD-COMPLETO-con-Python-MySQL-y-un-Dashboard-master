# Configuración con Variables de Entorno (.env)

## ✅ Configuración Completada

El proyecto ahora usa variables de entorno para las credenciales de MySQL. Esto es más seguro y flexible.

## 📁 Archivos Creados

1. **`.env`** - Archivo con tus credenciales de MySQL (NO se sube a Git)
2. **`.env.example`** - Plantilla de ejemplo para otros desarrolladores

## 🔧 Archivos Modificados

1. **`my-app/conexion/conexionBD.py`** - Ahora lee credenciales desde `.env`
2. **`crear_bd.py`** - Ahora lee credenciales desde `.env`
3. **`run.py`** - Carga las variables de entorno al inicio
4. **`requirements.txt`** - Agregado `python-dotenv==1.0.0`

## 📝 Cómo Configurar tus Credenciales

1. Abre el archivo `.env` en la raíz del proyecto
2. Edita los valores según tu configuración de MySQL:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña_real_aqui
MYSQL_PORT=3306
MYSQL_DATABASE=crud_python
```

3. Guarda el archivo

## ⚠️ Importante

- **NO subas el archivo `.env` a Git** - Ya está en `.gitignore`
- **Sí sube `.env.example`** - Es una plantilla sin credenciales reales
- Si cambias tus credenciales de MySQL, solo edita el archivo `.env`

## 🚀 Próximos Pasos

1. Edita el archivo `.env` con tus credenciales reales de MySQL
2. Crea la base de datos ejecutando:
   ```bash
   python crear_bd.py
   ```
3. Inicia la aplicación:
   ```bash
   python run.py
   ```

## ✅ Verificar Configuración

Puedes verificar que las variables de entorno se carguen correctamente ejecutando:
```bash
python test_env.py
```

