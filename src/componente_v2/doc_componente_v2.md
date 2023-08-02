1. Estructura del proyecto
Dentro del contenedor Docker, podrías tener la siguiente estructura de directorios:


/app
    /scripts
    /app
        main.py
    Dockerfile
    requirements.txt
Donde /scripts contiene todos los scripts que se van a ejecutar, main.py es la aplicación FastAPI principal que maneja las solicitudes, Dockerfile es para construir la imagen Docker y requirements.txt lista las dependencias de Python.

2. Dockerfile
El archivo Dockerfile podría tener un aspecto como el siguiente:

FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app/app
COPY ./scripts /app/scripts

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
Este Dockerfile utiliza la imagen base de Python 3.9, establece el directorio de trabajo en /app, instala las dependencias requeridas y copia los archivos de aplicación y scripts al contenedor. Finalmente, inicia la aplicación FastAPI utilizando Uvicorn.

3. Aplicación FastAPI
El archivo main.py podría verse algo como esto:

from fastapi import FastAPI, HTTPException
from subprocess import Popen, PIPE
import os

app = FastAPI()

@app.post("/execute_script/")
async def execute_script(script_name: str, script_parameters: str):
    if not os.path.isfile(f"/app/scripts/{script_name}"):
        raise HTTPException(status_code=404, detail="Script not found")

    process = Popen([f"/app/scripts/{script_name}", script_parameters], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise HTTPException(status_code=500, detail=stderr.decode())

    return {"output": stdout.decode()}
Este código FastAPI básicamente espera una solicitud POST a la ruta /execute_script/. Se espera que la solicitud contenga el nombre del script a ejecutar y los parámetros que deben pasarse al script.

Se comprueba si el script existe y, si es así, se ejecuta utilizando Popen. El stdout y stderr del script se capturan. Si el script se ejecuta con éxito, se devuelve el stdout. Si hay algún error, se devuelve el stderr.

4. Comunicación entre Access Manager y Processing Manager
Para comunicarse entre el Access Manager y el Processing Manager, puedes utilizar HTTP. FastAPI es compatible con los clientes HTTP modernos. Aquí tienes un ejemplo de cómo podría ser una solicitud desde Access Manager:

import requests

def send_script_to_process(script_name, script_parameters):
    response = requests.post("http://processing-manager:8000/execute_script/", data={"script_name": script_name, "script_parameters": script_parameters})

    if response.status_code == 200:
        print("Script processed successfully. Output:", response.json()["output"])
    else:
        print("Failed to process script. Error:", response.json()["detail"])
Este código hace una solicitud POST al endpoint /execute_script/ del Processing Manager y pasa el nombre del script y los parámetros como datos del formulario.

Debes tener en cuenta que esta es solo una guía básica y puede necesitar modificaciones para adaptarse a tus necesidades específicas. Adicionalmente, es importante implementar medidas de seguridad adecuadas, especialmente si planeas ejecutar scripts no confiables o recibir solicitudes de fuentes no confiables.