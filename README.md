Experimental API Demo Project
A production-ready REST API demo project showcasing DevSecOps best practices, including CI/CD, containerization, security scanning, and GitOps deployment.

Project Overview
This project implements a simple To-Do List API with the following features:

FastAPI-based REST API with CRUD operations

Comprehensive test suite with high code coverage

Structured JSON logging

Prometheus metrics for observability

Multi-stage Docker build with security best practices

Azure DevOps CI/CD pipeline with security scanning

Kubernetes deployment manifests

GitOps deployment strategy with ArgoCD

Repository Structure
api-experimental-prototype/
├── app/                    # API application code
│   ├── __init__.py
│   ├── main.py             # FastAPI application entry point
│   └── models.py           # Data models             
├── tests/                  # Test suite
├── k8s/                    # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── monitoring/         # Monitoring configuration
│       ├── prometheus.yaml
│       ├── prometheus-deployment.yaml
│       ├── grafana-deployment.yaml
│       └── api-dashboard.json
├── argocd/                 # ArgoCD configuration
│   └── application.yaml
├── Dockerfile              # Multi-stage Docker build
├── requirements.txt        # Python dependencies
├── openapi.json            # API specification
└── azure-pipelines.yml     # CI/CD pipeline configuration


Copy
API Endpoints
POST /tasks: Create a new task

GET /tasks: List all tasks

GET /tasks/{task_id}: Get a specific task

PUT /tasks/{task_id}: Update a task

DELETE /tasks/{task_id}: Delete a task

GET /health: Health check endpoint

GET /metrics: Prometheus metrics endpoint

Deployment Instructions
1. Local Development
Prerequisites
Python 3.11+

Docker

Setup
Clone the repository:

git clone https://github.com/yourusername/api-experimental-prototype.git
cd api-experimental-prototype

Copy
bash
Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Copy
bash
Run the application:

uvicorn app.main:app --reload

Copy
bash
Access the API documentation at http://localhost:8000/docs

Running Tests
pytest tests/ --cov=app

Copy
bash
2. Docker Deployment
Build and Run Locally
docker build -t experimental-api:latest .
docker run -p 8000:8000 experimental-api:latest

Copy
bash
Push to Container Registry
# For Docker Hub
docker tag experimental-api:latest yourusername/experimental-api:latest
docker push yourusername/experimental-api:latest

# For Azure Container Registry
az acr login --name yourregistry
docker tag experimental-api:latest yourregistry.azurecr.io/experimental-api:latest
docker push yourregistry.azurecr.io/experimental-api:latest

Copy
bash
3. Kubernetes Deployment (Manual)
Prerequisites
Kubernetes cluster (Minikube, AKS, EKS, etc.)

kubectl configured to access your cluster

Deploy the API
# Create namespace
kubectl create namespace experimental-api

# Apply Kubernetes manifests
kubectl apply -f k8s/deployment.yaml -n experimental-api
kubectl apply -f k8s/service.yaml -n experimental-api
kubectl apply -f k8s/configmap.yaml -n experimental-api

# Verify deployment
kubectl get pods -n experimental-api
kubectl get svc -n experimental-api

# Access the API (port-forward)
kubectl port-forward svc/experimental-api 8000:80 -n experimental-api

Copy
bash
4. Monitoring Setup
Prerequisites
Kubernetes cluster with Prometheus and Grafana

Deploy Monitoring Stack
# Create monitoring namespace
kubectl create namespace monitoring

# Deploy Prometheus
kubectl apply -f monitoring/prometheus.yaml -n monitoring
kubectl apply -f monitoring/prometheus-deployment.yaml -n monitoring

# Deploy Grafana
kubectl apply -f monitoring/grafana-deployment.yaml -n monitoring

# Wait for Grafana to be ready
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=120s

# Configure Prometheus as data source in Grafana
kubectl exec -it $(kubectl get pods -n monitoring -l app=grafana -o jsonpath='{.items[0].metadata.name}') -n monitoring -- \
  curl -s -X POST -H "Content-Type: application/json" -d '{"name":"prometheus","type":"prometheus","url":"http://prometheus:9090","access":"proxy","isDefault":true}' \
  http://admin:admin@localhost:3000/api/datasources

# Import dashboard
kubectl cp monitoring/api-dashboard.json monitoring/$(kubectl get pods -n monitoring -l app=grafana -o jsonpath='{.items[0].metadata.name}'):/tmp/dashboard.json
kubectl exec -it $(kubectl get pods -n monitoring -l app=grafana -o jsonpath='{.items[0].metadata.name}') -n monitoring -- \
  curl -s -X POST -H "Content-Type: application/json" -d @/tmp/dashboard.json \
  http://admin:admin@localhost:3000/api/dashboards/db

# Access Grafana
kubectl port-forward svc/grafana 3000:3000 -n monitoring


Copy
bash
5. GitOps Deployment with ArgoCD
Prerequisites
Kubernetes cluster

Git repository with your application code and Kubernetes manifests

Install ArgoCD
# Create ArgoCD namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

Copy
bash
Deploy Application with ArgoCD
# Apply ArgoCD application manifest
kubectl apply -f argocd/application.yaml

# Verify application status
kubectl get applications -n argocd

Copy
bash
Using ArgoCD UI
Access the ArgoCD UI at https://localhost:8080

Login with username admin and the password retrieved earlier

You should see your application in the dashboard

Click on the application to view deployment details

Use the "Sync" button to manually trigger a deployment if needed

6. CI/CD Pipeline Setup (Azure DevOps)
Prerequisites
Azure DevOps account

Azure Container Registry

Service connection to your Azure resources

Configure Pipeline
Import your repository into Azure DevOps

Create a new pipeline using the existing azure-pipelines.yml file

Configure the following variables:

pythonVersion: Python version to use (e.g., '3.12')

image_repository: Name of your container image repository

acrName: Name of your Azure Container Registry

Run the pipeline

The pipeline will:

Validate code with tests and security scans

Build and push the Docker image

Scan the container image for vulnerabilities

Run DAST security testing

Update the Kubernetes manifests with the new image tag

Commit the changes to trigger ArgoCD deployment

Security Features
SAST scanning with Bandit

SCA scanning with OSV Scanner

Container scanning with Trivy

DAST scanning with OWASP ZAP

Non-root user in Docker container

Security context in Kubernetes deployment

Resource limits in Kubernetes deployment

Security headers for web vulnerabilities

Observability
Structured JSON logging

Prometheus metrics

Health check endpoint

Kubernetes liveness and readiness probes

Grafana dashboards for visualization

Troubleshooting
Common Issues
API not accessible after deployment

Check pod status: kubectl get pods -n experimental-api

Check logs: kubectl logs -l app=experimental-api -n experimental-api

Verify service: kubectl get svc -n experimental-api

ArgoCD not syncing

Check application status: kubectl get applications -n argocd

View detailed status: kubectl describe application experimental-api -n argocd

Check ArgoCD logs: kubectl logs -l app.kubernetes.io/name=argocd-server -n argocd

Prometheus not collecting metrics

Verify target configuration: kubectl get configmap prometheus-config -n monitoring -o yaml

Check if API is exposing metrics: curl http://localhost:8000/metrics

Ensure service has correct annotations: prometheus.io/scrape: "true"

Contributing
Fork the repository

Create a feature branch: git checkout -b feature/your-feature

Commit your changes: git commit -am 'Add your feature'

Push to the branch: git push origin feature/your-feature

Submit a pull request