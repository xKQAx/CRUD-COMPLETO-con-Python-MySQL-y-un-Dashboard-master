# CRUD con Python MySQL y Dashboard

Aprende a desarrollar un sistema **CRUD** utilizando **Python** y **MySQL** mientras creas un impresionante panel de control interactivo. Este proyecto es ideal para quienes buscan gestionar datos de manera eficiente y construir aplicaciones dinámicas con una interfaz amigable.

## Vista previa 🗃

![Dashboard Login](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/master/Dashboard-python-login-urian-viera.png)

![Crear Usuario](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/master/dashboard-python-crear-user-urian-viera.png)

![Recuperar Contraseña](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/master/dashboard-python-recuperar-clave-urian-viera.png)

![Panel Principal](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/master/dashborad-python-home-urian-viera.png)

![Registrar Cliente](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/master/dashboard-python-registrar-cliente-urian-viera.png)

![Lista de Empleados](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/master/dashboard-python-lista-empleados-urian-viera.png)

![Lista de Usuarios](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/master/dashboard-python-lista-usuarios-urian-viera.png)

![Editar Perfil](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/master/dashboard-python-editar-perfil-urian-viera.png)

![Reporte de Empleados](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/master/dashboard-python-reporte-empleados-urian-viera.png)

---

## Requerimientos

Para ejecutar este proyecto, necesitas:

- **Python:** 3.8 o superior
- **MySQL:** 5.7 o superior (recomendado 8.0+)
- **Sistema Operativo:** Windows 10 o superior

---

## Instalación Rápida

Para una instalación completa paso a paso, consulta la [Guía de Instalación Completa](GUIA_INSTALACION.md).

### Resumen de Pasos

1. **Descargar el proyecto:**
   ```bash
   git clone https://github.com/urian121/CRUD-COMPLETO-con-Python-MySQL-y-un-Dashboard.git
   cd CRUD-COMPLETO-con-Python-MySQL-y-un-Dashboard
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv env
   .\env\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar MySQL:**
   - Descarga desde: https://downloads.mysql.com/archives/community/
   - Sigue el asistente de instalación

5. **Configurar variables de entorno:**
   - Copia `.env.example` a `.env`
   - Edita `.env` con tus credenciales de MySQL

6. **Crear base de datos:**
   ```bash
   python crear_bd.py
   ```

7. **Ejecutar la aplicación:**
   ```bash
   python run.py
   ```

8. **Acceder desde el navegador:**
   - Ingresa a: http://127.0.0.1:5600/

---

## Documentación

- [Guía de Instalación Completa](GUIA_INSTALACION.md) - Instalación paso a paso
- [Documentación Adicional](docs/) - Guías y comandos adicionales

## Estructura del Proyecto

```
CRUD-COMPLETO-con-Python-MySQL-y-un-Dashboard/
├── my-app/                    # Aplicación principal
│   ├── app.py                 # Configuración de Flask
│   ├── conexion/              # Módulo de conexión a BD
│   ├── controllers/           # Lógica de negocio
│   ├── routers/               # Rutas de la aplicación
│   ├── templates/             # Plantillas HTML
│   └── static/                # Archivos estáticos
├── docs/                      # Documentación
├── resources/                  # Recursos adicionales
├── .env                       # Variables de entorno (crear desde .env.example)
├── requirements.txt           # Dependencias
├── run.py                     # Script principal de inicio
├── crear_bd.py                # Script para crear la base de datos
└── verificar_mysql.py         # Script para verificar MySQL
```

---

## Expresiones de Gratitud

- **Comenta:** Comparte este proyecto con otros desarrolladores
- **Invita una cerveza o un café:** [Paypal](mailto:iamdeveloper86@gmail.com)
- **Da crédito:** Agradece en tus redes sociales

## Notas Finales

No olvides suscribirte y dejar tus comentarios. Este proyecto es una base que puedes mejorar y personalizar según tus necesidades.

**Autor:** Urian Viera

---

[Repositorio en GitHub](https://github.com/urian121/CRUD-COMPLETO-con-Python-MySQL-y-un-Dashboard)

Si encuentras útil este proyecto, dale una estrella en GitHub
