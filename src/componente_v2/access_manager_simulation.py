import subprocess
import json
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

RESULT_RETURN_URL = "http://host.docker.internal:8080/results"

app = FastAPI()

# @app.post("/run", status_code=202)
# async def run(command: DockerCommand, process: DockerProcess = Depends(DockerProcess)) -> dict:
#     if process.process.returncode is None:
#         return {"status": "started", "PID": process.process.pid}
#     else:
#         raise HTTPException(status_code=500, detail=f"Error occurred. PID: {process.process.pid}, Error code: {process.process.returncode}")

@app.post("/results", status_code=201)
async def receive_results(request: Request) -> dict:
    data = await request.json()
    if data:
        print(f"Script result: {data}")
        return {"status": "received", "data": data}
    else:
        raise HTTPException(status_code=400, detail="No data received")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)



