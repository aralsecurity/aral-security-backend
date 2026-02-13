from fastapi import FastAPI, UploadFile, File
import subprocess
import json
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ARAL Security Backend Running"}

@app.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    file_location = f"/tmp/{file.filename}"
    
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    result = subprocess.run(
        ["trivy", "config", "--format", "json", file_location],
        capture_output=True,
        text=True
    )

    os.remove(file_location)

    try:
        return json.loads(result.stdout)
    except:
        return {"error": "Scan failed", "details": result.stderr}
