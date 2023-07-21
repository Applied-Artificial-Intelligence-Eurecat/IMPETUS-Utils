import subprocess
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any
import uvicorn

# Define el nombre de tu imagen Docker y los argumentos que quieres pasar
# docker_image_name = "componente-v1.0"
# script_path = "calculos.py"
# args = "arg1 arg2 arg3"
# url = "http://host.docker.internal:8080/results"
# docker_command = f'docker run -e SCRIPT_PATH={script_path} -e ARGS="{args}" -e URL={url} {docker_image_name}'
docker_image_name = "componente-v1.0"
script_path = "calculos.py"
args = "arg1 arg2 arg3"
url = "http://host.docker.internal:8080/results"
docker_command = ["docker", "run", "-e", f"SCRIPT_PATH={script_path}", "-e", f'ARGS="{args}"', "-e", f'URL={url}', docker_image_name]

app = FastAPI()

class Item(BaseModel):
    data: Any

@app.post("/run")
async def run_docker(item: Item):
    print(docker_command)
    print(f'Sending subprocess to run... ')
    # process = subprocess.run(docker_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    process = subprocess.run(docker_command)
    print(f'Process: {process}')
    print(f' Process returncode: {process.returncode}')
    # return {"status": process.returncode}
    return {"status": 1000}

@app.post("/results")
async def receive_results(request: Request):
    data = await request.json()
    data = await request.body()
    data = json.loads(data)

    # Ahora "data" contiene los resultados que fueron enviados por el contenedor Docker
    # Hacer algo con los datos...
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)


