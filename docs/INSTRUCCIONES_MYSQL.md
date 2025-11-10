# Instrucciones para Instalar y Configurar MySQL

## Opción 1: Instalar MySQL Server (Recomendado)

### Paso 1: Descargar MySQL
1. Ve a: https://dev.mysql.com/downloads/mysql/
2. Descarga MySQL Installer para Windows
3. Selecciona la versión "mysql-installer-community" (gratuita)

### Paso 2: Instalar MySQL
1. Ejecuta el instalador descargado
2. Selecciona "Developer Default" o "Server only"
3. Durante la instalación:
   - Configura el puerto: **3306** (por defecto)
   - Establece la contraseña del usuario **root**: **password** (o la que prefieras)
   - Marca "Start MySQL Server at System Startup" para que inicie automáticamente

### Paso 3: Verificar la Instalación
Abre PowerShell como Administrador y ejecuta:
```powershell
Get-Service -Name "*mysql*"
```

### Paso 4: Iniciar el Servicio MySQL
Si el servicio no está corriendo, ejecuta:
```powershell
# Como Administrador
Start-Service MySQL80
# O el nombre que tenga tu servicio MySQL
```

### Paso 5: Crear la Base de Datos
Una vez que MySQL esté corriendo, ejecuta desde la raíz del proyecto:
```bash
python crear_bd.py
```

## Opción 2: Usar XAMPP (Más Fácil)

### Paso 1: Descargar XAMPP
1. Ve a: https://www.apachefriends.org/download.html
2. Descarga XAMPP para Windows
3. Instala XAMPP (incluye MySQL)

### Paso 2: Iniciar MySQL desde XAMPP
1. Abre el Panel de Control de XAMPP
2. Haz clic en "Start" junto a MySQL
3. El servicio MySQL estará corriendo en el puerto 3306

### Paso 3: Configurar la Contraseña
1. Abre phpMyAdmin desde XAMPP (http://localhost/phpmyadmin)
2. Ve a "Usuarios" → "root" → "Cambiar contraseña"
3. Establece la contraseña como **password** (o actualiza `conexionBD.py` con tu contraseña)

### Paso 4: Crear la Base de Datos
Ejecuta desde la raíz del proyecto:
```bash
python crear_bd.py
```

## Opción 3: Usar MySQL como Servicio de Windows

Si MySQL ya está instalado pero el servicio no está corriendo:

### Iniciar el Servicio Manualmente
```powershell
# Abre PowerShell como Administrador
net start MySQL80
# O el nombre que tenga tu servicio MySQL
```

### Configurar para Inicio Automático
```powershell
# Como Administrador
Set-Service -Name MySQL80 -StartupType Automatic
```

## Verificar que MySQL Está Corriendo

Ejecuta este comando para verificar:
```powershell
Get-Service -Name "*mysql*" | Select-Object Name, Status
```

El estado debe ser "Running".

## Probar la Conexión

Una vez que MySQL esté corriendo, prueba la conexión:
```bash
python my-app/test_conexion.py
```

## Nota sobre Credenciales

Si cambias la contraseña de MySQL, recuerda actualizar el archivo:
- `my-app/conexion/conexionBD.py` (línea 12: `passwd="tu_contraseña"`)
- `crear_bd.py` (línea 15: `MYSQL_PASSWORD = "tu_contraseña"`)

