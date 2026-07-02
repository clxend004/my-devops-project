# Deployment Strategy (Local → Staging)

## 1. Environment Structure

This document defines the deployment strategy used to transition the application from the **local development environment** to the **staging environment**.  
The purpose of this strategy is to ensure consistent deployment, testing, and validation of services before production release.

---

## Environment Overview

| Environment | Purpose | Services | Access |
|-------------|---------|----------|--------|
| **Local** | Used by developers for building, testing, and debugging the application on their own machines. | Frontend, Backend, Blockchain | Frontend → http://localhost:8080<br>Backend → http://localhost:5000<br>Blockchain → http://localhost:8545 |
| **Staging** | Used for integration testing before production deployment. It mirrors the production setup to validate system behavior. | Frontend, Backend, Blockchain | Access depends on deployment configuration |

---

## Local Environment

The **local environment** is used by developers to run and test application components during development.

Services are started using **Docker Compose**, which orchestrates the required containers.

### Services

- **Frontend** – User interface of the application  
- **Backend** – API and business logic service  
- **Blockchain** – Smart contract execution and blockchain interaction  

### Local Access URLs

| Service | URL |
|--------|-----|
| Frontend | http://localhost:8080 |
| Backend | http://localhost:5000 |
| Blockchain | http://localhost:8545 |

---

## Staging Environment

The **staging environment** is designed to replicate the production environment as closely as possible.

In this environment:

- Docker images are **built automatically through the CI pipeline**
- Images are **stored in the container registry**
- Deployment uses **pre-built container images**
- The full system integration is tested before production deployment

### Purpose of Staging

- Validate service integration
- Verify CI/CD deployment process
- Perform end-to-end testing
- Ensure system stability before production release

---

## Deployment Flow

Local Development → CI Pipeline → Docker Image Build → Container Registry → Staging Deployment

This workflow ensures that only validated builds are deployed to the staging environment.

---

# 2. Service Dependency Matrix

The following table describes the relationship between services in the system.

| Service | Depends On | Description |
|--------|-------------|-------------|
| Frontend | Backend | The frontend sends API requests to the backend service. |
| Backend | Blockchain | The backend interacts with smart contracts deployed on the blockchain. |
| Blockchain | None | The blockchain node runs independently and provides smart contract functionality. |

---

## Service Interaction Flow

User → Frontend → Backend → Blockchain

1. Users interact with the **Frontend** interface.
2. The **Frontend** sends requests to the **Backend API**.
3. The **Backend** processes logic and interacts with **Blockchain smart contracts**.
4. The **Blockchain** executes contract functions and returns results.

---

# 3. Deployment Instructions (Staging Environment)

The staging environment is deployed using Docker Compose and container images stored in the GitHub Container Registry.

## Step 1 – Ensure Docker is installed

Check Docker installation:

  docker --version

## Step 2 – Pull container images

Pull the latest images from the container registry:

 docker compose -f docker-compose.staging.yml pull
 
## Step 3 – Start the staging environment

Run the following command:

 docker compose -f docker-compose.staging.yml up -d
 
## Step 4 – Verify running containers

Check running containers:

docker ps


Expected containers:

- frontend-service  
- backend-service  
- blockchain-service  

## Step 5 – Access the services

Frontend  
http://localhost:8080

Backend  
http://localhost:5000

Blockchain  
http://localhost:8545



  
