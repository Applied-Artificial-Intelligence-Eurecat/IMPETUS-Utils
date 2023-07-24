import subprocess
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any
import uvicorn

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
    process = subprocess.Popen(docker_command)
    print(f'Process started with PID: {process.pid}')
    print(f'Process: {process}')
    print(f' Process returncode: {process.returncode}')
    return {"status": process.returncode}

@app.post("/results")
async def receive_results(request: Request):
    data = await request.body()
    data = json.loads(data)
    print(f"Data received through /results by subprocess: {data}")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)



