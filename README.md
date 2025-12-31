
---

```
# Contact Manager API

The Contact Manager API is a RESTful service for managing contacts using FastAPI and MongoDB, fully containerized with Docker and deployed on Kubernetes.

## Project Goals
- Build a REST API for CRUD operations on contacts.
- Use FastAPI as the backend framework.
- Store data in MongoDB.
- Package and run the system using Docker.
- Deploy the API and database on Kubernetes.
- Understand how Pods and Services communicate inside a cluster.

## Technologies
- Python 3.11
- FastAPI
- MongoDB 7
- Docker & Docker Compose
- Kubernetes (kubectl)

## Project Structure
(You may add your folder structure here if needed)

## Installation & Running

### 1. Prepare Environment
- Install Docker and Kubernetes (minikube or any cluster).
- Ensure kubectl is configured correctly.

### 2. Build & Push Docker Image
```bash
docker build -t elazarmeijers/contacts-api:v1 .
docker push elazarmeijers/contacts-api:v1
```

### 3. Deploy to Kubernetes
```bash
kubectl apply -f k8s/mongodb-pod.yaml
kubectl apply -f k8s/mongodb-service.yaml
kubectl apply -f k8s/api-pod.yaml
kubectl apply -f k8s/api-service.yaml
```

### 4. Verify Deployment
```bash
kubectl get pods
kubectl get services
kubectl logs api
```

## Example Request
POST /contacts
```json
{
    "first_name": "moshe",
    "last_name": "berkowich",
    "phone_number": "0501234567"
}
```

## Architecture Diagram
```
[User]
   |
   v
[API Service - NodePort:30080]
   |
   v
[API Pod]
   |
   v
[MongoDB Service - 27017]
   |
   v
[MongoDB Pod]
```

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|--------|-----------|
| API Pod can't reach MongoDB | Wrong Service name | Ensure MONGO_HOST matches the Service name |
| MongoDB Pod CrashLoopBackOff | Missing env vars | Check required MongoDB environment variables |
| API not accessible externally | Service type is ClusterIP | Change to NodePort or use Ingress |
```

---
