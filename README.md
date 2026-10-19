# proyecto_mongodb
# Sistema Administrativo y de Gestión - STI-RAG (Panel Web Cloud)

Plataforma Full Stack desarrollada para la administración, control y seguimiento de expedientes estudiantiles en el marco del **Sistema de Tutoría Inteligente basado en Generación Aumentada por Recuperación (STI-RAG)**, enfocada en la evaluación y diagnóstico de la alfabetización funcional.

## 🚀 Características Principales
- **Arquitectura Cloud Distribuida:** Despliegue activo en la nube mediante **Render** con persistencia NoSQL escalable alojada en **MongoDB Atlas**.
- **Backend de Alto Rendimiento:** API RESTful construida con **Python y FastAPI** para un procesamiento asíncrono eficiente.
- **Autenticación y Seguridad Segura:** Sistema de verificación de doble factor mediante códigos únicos (OTP) e inicio de sesión protegido.
- **Panel de Control Reactivo (CRUD):** Interfaz web responsiva para la gestión en tiempo real (Crear, Leer, Actualizar y Eliminar) de registros estudiantiles.
- **Monitoreo en Vivo:** Indicador dinámico de estado y salud del servidor (*Health Check*) enlazado con la base de datos en la nube.

## 🛠️ Tecnologías Utilizadas
- **Backend:** Python, FastAPI, Pydantic, PyMongo, Uvicorn.
- **Base de Datos:** MongoDB Atlas (NoSQL - Colecciones `usuarios` y `estudiantes`).
- **Frontend:** HTML5, CSS3, JavaScript asíncrono (Fetch API).
- **Infraestructura y Despliegue:** Render (Cloud PaaS), GitHub (CI/CD Auto-Deploy).
