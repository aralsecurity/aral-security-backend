from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess
import json
import os
import uuid

app = FastAPI()

# Templates & Static
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None,
            "error": None
        }
    )


@app.post("/scan", response_class=HTMLResponse)
async def scan_file(request: Request, file: UploadFile = File(...)):

    # Create unique temp filename
    temp_filename = f"{uuid.uuid4()}_{file.filename}"
    file_location = os.path.join(os.getcwd(), temp_filename)

    try:
        # Save uploaded file
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        print(f"Scanning file: {file_location}")

        # Run Trivy
        result = subprocess.run(
            ["tools/trivy.exe", "config", "--format", "json", file_location],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "result": None,
                    "error": result.stderr
                }
            )

        data = json.loads(result.stdout)

        # Severity counters
        critical = 0
        high = 0
        medium = 0
        low = 0
        findings = []

        for r in data.get("Results", []):
            for mis in r.get("Misconfigurations", []):

                severity = mis.get("Severity", "")

                if severity == "CRITICAL":
                    critical += 1
                elif severity == "HIGH":
                    high += 1
                elif severity == "MEDIUM":
                    medium += 1
                elif severity == "LOW":
                    low += 1

                findings.append({
                    "id": mis.get("ID"),
                    "title": mis.get("Title"),
                    "severity": severity
                })

        total = critical + high + medium + low

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": {
                    "critical": critical,
                    "high": high,
                    "medium": medium,
                    "low": low,
                    "total": total,
                    "findings": findings
                },
                "error": None
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": str(e)
            }
        )

    finally:
        # Always clean temp file
        if os.path.exists(file_location):
            os.remove(file_location)
