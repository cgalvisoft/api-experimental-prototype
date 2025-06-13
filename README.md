# Experimental API Demo Project

A production-ready REST API demo project showcasing DevSecOps best practices, including CI/CD, containerization, security scanning, and GitOps deployment.

## Project Overview

This project implements a simple To-Do List API with the following features:

- FastAPI-based REST API with CRUD operations
- Comprehensive test suite with high code coverage
- Structured JSON logging
- Prometheus metrics for observability
- Multi-stage Docker build with security best practices
- Azure DevOps CI/CD pipeline with security scanning
- Kubernetes deployment manifests
- GitOps deployment strategy with ArgoCD

## API Endpoints

- `POST /tasks`: Create a new task
- `GET /tasks`: List all tasks
- `GET /tasks/{task_id}`: Get a specific task
- `PUT /tasks/{task_id}`: Update a task
- `DELETE /tasks/{task_id}`: Delete a task
- `GET /health`: Health check endpoint
- `GET /metrics`: Prometheus metrics endpoint

## Local Development

### Prerequisites

- Python 3.11+
- Docker

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/api-experimental-prototype.git
   cd api-experimental-prototype
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Access the API documentation at http://localhost:8000/docs

### Running Tests

```bash
pytest tests/ --cov=app
```

## Docker Build

```bash
docker build -t experimental-api:latest .
docker run -p 8000:8000 experimental-api:latest
```

## CI/CD Pipeline

The project includes an Azure DevOps pipeline (`azure-pipelines.yml`) with the following stages:

1. **Validate**: Run tests, code coverage, and security scans
2. **Build and Push**: Build and push the Docker image to Azure Container Registry
3. **Scan Image**: Scan the container image for vulnerabilities

## GitOps Deployment with ArgoCD

### Setting up ArgoCD

1. Install ArgoCD in your Kubernetes cluster:
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

2. Access the ArgoCD UI:
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```

3. Login with the default admin credentials (username: admin, password: retrieve with `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`)

### Creating an ArgoCD Application

1. Create an Application manifest:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: experimental-api
     namespace: argocd
   spec:
     project: default
     source:
       repoURL: https://github.com/yourusername/api-experimental-prototype.git
       targetRevision: HEAD
       path: k8s
     destination:
       server: https://kubernetes.default.svc
       namespace: experimental-api
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
   ```

2. Apply the manifest:
   ```bash
   kubectl apply -f argocd-application.yaml
   ```

### CI/CD Integration with GitOps

In a real-world scenario, the CI pipeline should be modified to:

1. Build and push the Docker image with a unique tag (e.g., commit SHA or build ID)
2. Update the image tag in the Kubernetes manifests
3. Commit and push the updated manifests to the Git repository

This can be achieved by adding a step to the Azure DevOps pipeline:

```yaml
- script: |
    # Clone the repository
    git clone https://github.com/yourusername/api-experimental-prototype.git
    cd api-experimental-prototype
    
    # Update the image tag in the deployment manifest
    sed -i "s|\${IMAGE_TAG}|$(image_tag)|g" k8s/deployment.yaml
    sed -i "s|\${ACR_NAME}|$(acr_name)|g" k8s/deployment.yaml
    
    # Configure Git
    git config --global user.email "ci@example.com"
    git config --global user.name "CI Pipeline"
    
    # Commit and push changes
    git add k8s/deployment.yaml
    git commit -m "Update image to $(image_tag)"
    git push
  displayName: 'Update deployment manifest'
```

ArgoCD will detect the changes in the Git repository and automatically deploy the updated application.

## Security Features

- SAST scanning with Bandit
- SCA scanning with OSV Scanner
- Container scanning with Trivy
- Non-root user in Docker container
- Security context in Kubernetes deployment
- Resource limits in Kubernetes deployment

## Observability

- Structured JSON logging
- Prometheus metrics
- Health check endpoint
- Kubernetes liveness and readiness probes