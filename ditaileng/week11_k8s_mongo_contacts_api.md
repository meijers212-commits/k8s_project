# **Week 11 Project: Contact Manager API with Kubernetes**

## **Table of Contents**

1. **Project Objectives**  
2. **Project Overview**  
3. **Functional Requirements**  
   - 3.1 Data Model  
   - 3.2 API Endpoints  
4. **Technical Requirements**
   - 4.1 Required Project Structure
   - 4.2 Class Design Requirements
   - 4.3 Docker Requirements
   - 4.4 Kubernetes Requirements
   - 4.5 Bonus: Environment Variables with .env File (+10 points)  
5. **Git & Documentation Requirements**  
   - 5.1 Git Requirements  
   - 5.2 Documentation Requirements  
6. **Testing Requirements**  
7. **Submission Guidelines**  
   - 7.1 What to Submit  
   - 7.2 Submission Checklist  
   - 7.3 Testing Your Submission  
8. **Recommended Timeline**  
   - 8.1 Day 1 (6 hours)  
   - 8.2 Day 2 (6 hours)  
9. **Resources**  
10. **Frequently Asked Questions**  
11. **Important Notes**

---

## 1\. Project Objectives

By completing this project, you will demonstrate:

- **Object-Oriented Programming** – Designing and implementing Python classes  
- **NoSQL Database Operations** – Working with MongoDB using PyMongo  
- **API Development** – Creating REST endpoints with FastAPI  
- **Containerization** – Building Docker images for your application  
- **Container Orchestration** – Deploying applications with Kubernetes Pods and Services

---

## 2\. Project Overview

You will build a **Contact Manager API** – a REST API service that allows users to manage a contact list. The application will:

- Store contacts in a MongoDB database  
- Provide HTTP endpoints for CRUD operations (Create, Read, Update, Delete)  
- Run as containers orchestrated by Kubernetes  
- Use Kubernetes Services for networking between components

**Technology Stack:**

- Python 3.11+  
- FastAPI (web framework)  
- MongoDB 7.0 (database)  
- Docker (containerization)  
- Kubernetes (orchestration)

**Duration:** 2 days

---

## 3\. Functional Requirements

### 3.1 Data Model

Each contact must have the following fields:

| Field | Type | Constraints |
| :---- | :---- | :---- |
| \_id | ObjectId | Primary Key (auto-generated) |
| first\_name | String (50 chars) | Required |
| last\_name | String (50 chars) | Required |
| phone\_number | String (20 chars) | Required, Unique |

### 3.2 API Endpoints

Your API must implement these 4 endpoints:

| Method | Endpoint | Description | Request Body | Response |
| :---- | :---- | :---- | :---- | :---- |
| GET | `/contacts` | Get all contacts | None | List of all contacts |
| POST | `/contacts` | Create new contact | Contact data | Success message \+ ID |
| PUT | `/contacts/{id}` | Update existing contact | Updated fields | Success message |
| DELETE | `/contacts/{id}` | Delete contact | None | Success message |

**Example Request/Response:**

\# Create a contact

POST /contacts

{

    "first\_name": "John",

    "last\_name": "Doe",

    "phone\_number": "050-1234567"

}

\# Response

{

    "message": "Contact created successfully",

    "id": "507f1f77bcf86cd799439011"

}

---

## 4\. Technical Requirements

### 4.1 Required Project Structure

week11\_k8s\_contacts/

├── .gitignore
├── README.md
├── app/
│   ├── .env                     \# Environment variables (optional - see bonus)
│   ├── .env.example             \# Environment template (optional - see bonus)
│   ├── Dockerfile
│   ├── main.py                  \# FastAPI application
│   ├── data\_interactor.py       \# MongoDB connection \+ CRUD operations
│   └── requirements.txt
└── k8s/
    ├── mongodb-pod.yaml         \# MongoDB Pod definition
    ├── mongodb-service.yaml     \# MongoDB Service definition
    ├── api-pod.yaml             \# API Pod definition
    └── api-service.yaml         \# API Service definition

**Note:** The `.env` and `.env.example` files are optional and relate to the bonus requirement below.

### 4.2 Class Design Requirements

You must implement the following:

1. **Contact Class**  
     
   - Properties: id, first\_name, last\_name, phone\_number  
   - Method to convert contact to dictionary format

   

2. **Data Interactor Class/Module** (`data_interactor.py`)  
     
   This file should handle **both** the MongoDB connection AND all CRUD operations:  
     
   - Create MongoDB connection (using environment variables for host/port)  
   - `create_contact(contact_data: dict)` → returns new contact ID as string  
   - `get_all_contacts()` → returns list of Contact objects  
   - `update_contact(id: str, contact_data: dict)` → returns success boolean  
   - `delete_contact(id: str)` → returns success boolean

   

3. **FastAPI Application** (`main.py`)  
     
   - Define request/response models using Pydantic  
   - Implement 4 API endpoints  
   - Handle errors with appropriate HTTP status codes

### 4.3 Docker Requirements

**Application Dockerfile** (`app/Dockerfile`)

- Base image: `python:3.11-slim`  
- Install dependencies from requirements.txt  
- Copy application code  
- Expose port 8000  
- Run uvicorn server

**Example Dockerfile:**

FROM python:3.11-slim  
WORKDIR /app  
COPY requirements.txt .  
RUN pip install \--no-cache-dir \-r requirements.txt  
COPY . .  
EXPOSE 8000  
CMD \["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"\]

**Building and Pushing:**

After creating your Dockerfile, you will need to:
1. Build the Docker image with an appropriate tag (include your Docker Hub username)
2. Login to Docker Hub
3. Push the image to your Docker Hub registry

**Note:** Make sure you have a Docker Hub account and are logged in before pushing. You'll reference this image in your Kubernetes Pod manifest.

### 4.4 Kubernetes Requirements

You need to create **4 YAML files** – two Pods and two Services. Research Kubernetes Pod and Service manifests to build these files.

#### 1\. MongoDB Pod (`k8s/mongodb-pod.yaml`)

Create a Pod manifest for MongoDB with the following requirements:

- **API version**: v1
- **Kind**: Pod
- **Metadata**:
  - Name: `mongodb`
  - Labels: Include `app: mongodb` (used by Service selector)
- **Container specifications**:
  - Container name: `mongodb`
  - Image: `mongo:7.0` (official MongoDB image)
  - Container port: `27017` (MongoDB's default port)
  - Environment variables:
    - `MONGO_INITDB_DATABASE` set to `"contactsdb"`

**Purpose:** This Pod runs a MongoDB container that will store your contacts data.

#### 2\. MongoDB Service (`k8s/mongodb-service.yaml`)

Create a Service manifest for MongoDB with the following requirements:

- **API version**: v1
- **Kind**: Service
- **Metadata**:
  - Name: `mongodb-service`
- **Service specifications**:
  - Selector: `app: mongodb` (matches the Pod label)
  - Port: `27017`
  - Target port: `27017`
  - Type: `ClusterIP` (internal-only access)

**Purpose:** This Service provides a stable network endpoint for MongoDB. Your API will connect using the hostname `mongodb-service`.

#### 3\. API Pod (`k8s/api-pod.yaml`)

Create a Pod manifest for your API with the following requirements:

- **API version**: v1
- **Kind**: Pod
- **Metadata**:
  - Name: `api`
  - Labels: Include `app: api` (used by Service selector)
- **Container specifications**:
  - Container name: `api`
  - Image: `<your-dockerhub-username>/contacts-api:v1` (replace with your Docker Hub username)
  - Image pull policy: `Always` (ensures Kubernetes pulls from registry)
  - Container port: `8000`
  - Environment variables (CRITICAL - API needs these to connect to MongoDB):
    - `MONGO_HOST` set to `"mongodb-service"`
    - `MONGO_PORT` set to `"27017"`
    - `MONGO_DB` set to `"contactsdb"`

**Purpose:** This Pod runs your FastAPI application. The environment variables tell your API how to connect to MongoDB.

#### 4\. API Service (`k8s/api-service.yaml`)

Create a Service manifest for your API with the following requirements:

- **API version**: v1
- **Kind**: Service
- **Metadata**:
  - Name: `api-service`
- **Service specifications**:
  - Selector: `app: api` (matches the Pod label)
  - Port: `8000`
  - Target port: `8000`
  - Node port: `30080` (external access port)
  - Type: `NodePort` (allows external access)

**Purpose:** This Service exposes your API to the outside world, making it accessible from your browser or curl commands.

**Resources for YAML creation:**
- Kubernetes Pods: https://kubernetes.io/docs/concepts/workloads/pods/
- Kubernetes Services: https://kubernetes.io/docs/concepts/services-networking/service/
- YAML syntax reference: https://kubernetes.io/docs/reference/

### 4.5 Bonus Requirement: Environment Variables with .env File (+10 points)

**BONUS:** Instead of hardcoding environment variables in your code, use a `.env` file for local development.

**Requirements:**

1. **Create `app/.env` file** with environment variables:
   ```
   MONGO_HOST=localhost
   MONGO_PORT=27017
   MONGO_DB=contactsdb
   ```

2. **Load environment variables** in your `data_interactor.py`:
   - Use a library like `python-dotenv` to load variables from `.env` file
   - Add `python-dotenv` to your `requirements.txt`
   - Variables should be loaded automatically when running locally

3. **Add `.env` to .gitignore** (DO NOT commit .env file)

4. **Create `.env.example`** file with template (without sensitive values):
   ```
   MONGO_HOST=localhost
   MONGO_PORT=27017
   MONGO_DB=contactsdb
   ```

**Why this is useful:**
- Separates configuration from code
- Makes it easy to switch between local and production environments
- Follows best practices for application configuration

**Note:** When running in Kubernetes, the Pod's environment variables (defined in `api-pod.yaml`) will override the `.env` file values.

---

## Understanding the Architecture

![][image1]

**Key Concepts:**

1. **Pods** are the smallest deployable units – they run your containers  
2. **Services** provide stable networking – Pods can come and go, but Service names stay the same  
3. **ClusterIP** Services are internal-only (MongoDB doesn't need external access)  
4. **NodePort** Services are accessible from outside (so you can call your API)

---

## 5\. Git & Documentation Requirements

### 5.1 Git Requirements

1. **Repository Setup**

   - Create a GitHub repository named `week11_k8s_contacts`
   - Include `.gitignore` excluding:
     - `__pycache__/`
     - `*.pyc`
     - `.env`



2. **Branching Strategy** (**REQUIRED**)

   You must use a two-branch workflow:

   - **`main` branch**: Production-ready code only
     - This branch should contain only stable, tested code
     - Final submission should be on this branch

   - **`development` branch**: Active development work
     - Create this branch from `main`
     - Do all your development work on this branch
     - Commit frequently as you work
     - When features are complete and tested, merge to `main`

   **Workflow:**
   1. Create and switch to `development` branch
   2. Develop and commit your code on `development`
   3. Test everything thoroughly on `development`
   4. When ready, merge `development` into `main`
   5. Submit the repository with both branches visible



3. **Commit Standards**

   - Clear commit messages describing what changed
   - Commit often (especially on `development` branch)



4. **Suggested Commit Flow**  
     
   - "Initial project structure"  
   - "Implement Contact class"  
   - "Add MongoDB connection and CRUD operations"  
   - "Implement API endpoints"  
   - "Add Dockerfile"  
   - "Add Kubernetes manifests"  
   - "Add documentation"

### 5.2 Documentation Requirements

Your `README.md` must include:

1. **Project Description** – What the project does \+ API endpoints  
     
2. **Prerequisites:**  
     
   - Docker  
   - minikube (or other local Kubernetes)  
   - kubectl

   

3. **Setup Instructions** – How to build and deploy  
     
4. **Testing Instructions** – curl commands for each endpoint

---

## 6\. Testing Requirements

You must test and verify:

1. **Pods Running**

   - Verify both pods are in "Running" status
   - Check that MongoDB pod starts successfully
   - Check that API pod starts successfully

2. **Services Created**

   - Verify mongodb-service exists and is accessible
   - Verify api-service exists and is accessible
   - Confirm services are routing traffic to the correct pods

3. **CRUD Operations**

   - Test GET endpoint to retrieve all contacts
   - Test POST endpoint to create a new contact
   - Test PUT endpoint to update an existing contact
   - Test DELETE endpoint to remove a contact
   - All 4 endpoints should work correctly



4. **Error Handling**

   - Updating non-existent contact returns 404
   - Deleting non-existent contact returns 404

---

## 7\. Submission Guidelines

### 7.1 What to Submit

Submit your GitHub repository URL via MOODLE.

### 7.2 Submission Checklist

- [ ] Repository is public and accessible
- [ ] Repository has both `main` and `development` branches
- [ ] Final stable code is on `main` branch
- [ ] README.md contains setup and testing instructions
- [ ] .gitignore file exists and includes `.env`
- [ ] All required files present
- [ ] Docker image builds successfully
- [ ] All 4 Kubernetes manifests are valid
- [ ] All 4 API endpoints work correctly

### 7.3 Testing Your Submission

Before submitting, test your project end-to-end:

1. **Clone your repository** to a clean directory

2. **Build and push Docker image** to your Docker Hub registry

3. **Start your Kubernetes cluster** (minikube or other)

4. **Deploy all resources** to Kubernetes:
   - Deploy MongoDB Pod
   - Deploy MongoDB Service
   - Deploy API Pod
   - Deploy API Service

5. **Wait for pods to be ready** (typically 30-60 seconds)
   - Verify both pods show "Running" status

6. **Get the API URL** from your Kubernetes cluster

7. **Test all CRUD endpoints:**
   - Test GET /contacts (should return empty list initially)
   - Test POST /contacts to create a new contact
   - Test GET /contacts again (should show the created contact)
   - Test PUT /contacts/{id} to update the contact
   - Test DELETE /contacts/{id} to remove the contact

8. **Verify error handling:**
   - Try to update a non-existent contact (should return 404)
   - Try to delete a non-existent contact (should return 404)

9. **Clean up resources** when done testing

---

## 8\. Recommended Timeline

### 8.1 Day 1 (6 hours)

**Hours 1-2: Setup and Database Layer**

- Create GitHub repository
- Create `development` branch and switch to it
- Set up project structure
- Implement Contact class
- Implement data\_interactor.py with MongoDB connection and CRUD
- Commit your work on `development` branch

**Hours 3-4: API Development**

- Create requirements.txt  
- Implement FastAPI application  
- Implement all 4 endpoints  
- Test locally (run MongoDB in Docker, API locally)

**Hours 5-6: Dockerize**

- Create Dockerfile
- Build and test Docker image
- Test API container with MongoDB container

### 8.2 Day 2 (6 hours)

**Hours 1-2: Kubernetes Basics**

- Start your Kubernetes cluster
- Create mongodb-pod.yaml and mongodb-service.yaml
- Deploy and verify MongoDB is running

**Hours 3-4: Deploy API**

- Build and push image to Docker Hub registry
- Create api-pod.yaml and api-service.yaml
- Deploy and test API

**Hours 5-6: Testing and Documentation**

- Test all endpoints thoroughly
- Complete README.md
- Final testing on `development` branch
- Merge `development` branch into `main` branch
- Verify everything works on `main` branch
- Push both branches to GitHub
- Submit repository URL

---

## 9\. Resources

### Recommended Material

- FastAPI Basics: [https://fastapi.tiangolo.com/tutorial/first-steps/](https://fastapi.tiangolo.com/tutorial/first-steps/)  
- PyMongo Tutorial: [https://pymongo.readthedocs.io/en/stable/tutorial.html](https://pymongo.readthedocs.io/en/stable/tutorial.html)  
- Kubernetes Pods: [https://kubernetes.io/docs/concepts/workloads/pods/](https://kubernetes.io/docs/concepts/workloads/pods/)  
- Kubernetes Services: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)  
- minikube Start: [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/)

### Example Code Snippets

**MongoDB Connection in data\_interactor.py:**

import os

from pymongo import MongoClient

\# Read from environment variables (set in Kubernetes Pod)

MONGO\_HOST \= os.getenv("MONGO\_HOST", "localhost")

MONGO\_PORT \= os.getenv("MONGO\_PORT", "27017")

MONGO\_DB \= os.getenv("MONGO\_DB", "contactsdb")

\# Create connection

client \= MongoClient(f"mongodb://{MONGO\_HOST}:{MONGO\_PORT}/")

db \= client\[MONGO\_DB\]

contacts\_collection \= db\["contacts"\]

**Converting ObjectId for API responses:**

from bson import ObjectId

def contact\_to\_dict(contact):

    return {

        "id": str(contact\["\_id"\]),  \# Convert ObjectId to string

        "first\_name": contact\["first\_name"\],

        "last\_name": contact\["last\_name"\],

        "phone\_number": contact\["phone\_number"\]

    }

---

## 10\. Frequently Asked Questions

**Q: Can I use Docker Desktop's Kubernetes instead of minikube?** A: Yes\! Just make sure to adjust the image pull policy and access method accordingly.

**Q: What if my API can't connect to MongoDB?** A: Check that:

1. MongoDB pod is running (verify pod status)
2. MongoDB service exists (verify service status)
3. Your API uses `mongodb-service` as the host (not `localhost`)
4. Both pods are in the same namespace (default)

**Q: How do I see logs if something isn't working?** A: Use the appropriate command to view pod logs for both the API and MongoDB pods.

**Q: My API pod keeps crashing. How do I debug?** A: Check the pod logs and describe the pod to see detailed information about its status and any errors.

**Q: Do I need to use Deployments instead of Pods?** A: For this project, simple Pods are sufficient. Deployments add features like automatic restarts and scaling, but add complexity.

**Q: Will my data persist if I delete the MongoDB pod?** A: No. Without a PersistentVolume, data is lost when the pod is deleted. This is acceptable for this learning project.

**Q: Can I run the API locally (for development) but connect to MongoDB in Kubernetes?** A: Yes\! You have two options:

1. **Port Forwarding (Recommended):** Create a tunnel from your localhost to the Kubernetes MongoDB service on port 27017. Then set `MONGO_HOST=localhost` when running the API locally.

2. **NodePort Service:** Modify `mongodb-service.yaml` to use `type: NodePort` with a nodePort (e.g., 30017). Get your cluster's IP address and set `MONGO_HOST=<cluster-ip>` and `MONGO_PORT=30017`.

Port forwarding is simpler as it doesn't require modifying your YAML files.

---

## 11\. Important Notes

### Local Development with Kubernetes MongoDB

**IMPORTANT:** If you want to run your API locally (in your development environment) while connecting to MongoDB running in Kubernetes, you **MUST** create a tunnel or expose the MongoDB service. By default, Kubernetes services are only accessible within the cluster.

**Two Options:**

1. **Port Forwarding (Create a Tunnel):**
   - Create a port-forward tunnel from your localhost to the Kubernetes MongoDB service
   - This makes the MongoDB service accessible at `localhost:27017`
   - The port-forward session must remain active in a terminal while you develop

2. **NodePort (Expose via Cluster IP):**
   - Change the MongoDB service type from `ClusterIP` to `NodePort`
   - This binds a port (30000-32767 range) on the cluster node that's accessible from your host machine
   - Access MongoDB using the cluster's IP address and the NodePort
   - You'll need to find your cluster's IP address

**Note:** For the assignment submission, use the standard ClusterIP configuration (both API and MongoDB running in Kubernetes). The above is only for local development/testing.

### Common Mistakes to Avoid

❌ Using `localhost` as MongoDB host **when both API and MongoDB are in Kubernetes** (use `mongodb-service`)
❌ Forgetting to apply the Service before testing connectivity
❌ Not waiting for pods to be fully running before testing
❌ Not pushing the Docker image to registry before deploying
❌ Using incorrect Docker Hub username in the image reference
❌ Trying to connect local API to Kubernetes MongoDB without port-forward or NodePort

✅ Always check pod status before testing
✅ Use pod logs to debug issues
✅ Test MongoDB service first before deploying API
✅ Ensure you're logged into Docker Hub before pushing
✅ Commit code regularly
✅ Use port forwarding if testing API locally with K8s MongoDB

### Command Reference Notes

Students should research and include the appropriate CLI commands in their README.md for:

**Docker Commands:**
- Login to Docker Hub
- Build Docker images
- Push images to registry

**Kubernetes Commands:**
- Apply/create resources from YAML files
- Get/list resources (pods, services)
- View pod logs
- Describe resources for debugging
- Delete resources

**Minikube Commands:**
- Start/stop cluster
- Get service URLs
- Get cluster IP address

**Testing Commands:**
- Make HTTP requests to test API endpoints (GET, POST, PUT, DELETE)

Refer to official documentation:
- Docker CLI: https://docs.docker.com/engine/reference/commandline/cli/
- kubectl: https://kubernetes.io/docs/reference/kubectl/
- minikube: https://minikube.sigs.k8s.io/docs/commands/

---

Good luck\! Start with getting MongoDB running first, then add the API. Test at each step\!  
