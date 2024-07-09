FROM python:3.11-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y ffmpeg gcc

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . .

# Copia el archivo requirements.txt y instala las dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# Comando para iniciar tu aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]