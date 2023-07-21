# Usar una imagen base de Python 3.8
FROM python:3.8

# Establecer un directorio de trabajo
WORKDIR /app

# Instalar cualquier dependencia necesaria
# Copia el archivo de requerimientos y luego instala con pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el resto de los archivos
COPY . .

# Comando a ejecutar cuando se inicie el contenedor
CMD ["python", "componente_v1.py"]