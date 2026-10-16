# Usar una imagen oficial de Python
FROM python:3.10-slim

# Crear la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar tus archivos al contenedor
COPY requirements.txt .
COPY main.py .

# Instalar las librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 8000
EXPOSE 8000

# El comando automático para encender el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]