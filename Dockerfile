FROM python:3.12-slim

# Evita archivos .pyc y buffers
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar compiladores y dependencias necesarias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar las dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto para Gunicorn
EXPOSE 8000

# Comando por defecto para levantar el servidor
CMD ["gunicorn", "Concesionario.wsgi:application", "--bind", "0.0.0.0:8000"]