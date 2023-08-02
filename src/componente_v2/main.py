from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from subprocess import Popen, PIPE
import requests
import os

app = FastAPI()

class ScriptInput(BaseModel):
    script_name: str
    script_parameters: str

@app.post("/execute_script/")
async def execute_script(input: ScriptInput):
    print('a')
    # if not os.path.isfile(f"/app/procedures/{script_name}"):
    #     raise HTTPException(status_code=404, detail="Script not found")

    # process = Popen([f"/app/procedures/{script_name}", script_parameters], stdout=PIPE, stderr=PIPE)
    # stdout, stderr = process.communicate()

    # if process.returncode != 0:
    #     raise HTTPException(status_code=500, detail=stderr.decode())

    # return {"output": stdout.decode()}

# def send_script_to_process(script_name, script_parameters):
#     response = requests.post("http://processing-manager:8000/execute_script/", data={"script_name": script_name, "script_parameters": script_parameters})

#     if response.status_code == 200:
#         print("Script processed successfully. Output:", response.json()["output"])
#     else:
#         print("Failed to process script. Error:", response.json()["detail"])

