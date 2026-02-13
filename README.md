# Aral Security

Aral Security is a DevSecOps platform designed to scan Kubernetes and infrastructure configurations for security misconfigurations.

## 🚀 Features
- YAML file scanning
- Kubernetes misconfiguration detection
- Trivy integration
- Severity classification (LOW, MEDIUM, HIGH)
- JSON security report output

## 🛠 Tech Stack
- FastAPI
- Trivy
- Docker
- Python 3.14

## 📦 Run Locally

python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## 📌 Vision
To build a scalable DevSecOps SaaS platform for automated security scanning of infrastructure and applications.
