# DEV-W1-T3 – Minikube / Local Kubernetes Validation

## 📌 Task Overview

Validate a local Kubernetes environment using Minikube by:

- Installing and configuring Minikube
- Deploying at least one containerized service
- Verifying pod health
- Exposing service
- Documenting startup and teardown commands

---

## 🧰 Environment Setup

### Prerequisites

- Docker installed
- kubectl installed
- Minikube installed

Verify installations:

```bash
docker --version
kubectl version --client
minikube version
```

---

## 🚀 Cluster Startup

Start Minikube cluster:

```bash
minikube start
```

Verify cluster status:

```bash
minikube status
```

Check nodes:

```bash
kubectl get nodes
```

Expected output:
```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   ...   ...
```

---

## 📦 Deploy Containerized Service

Example: Deploy Backend Service

### Step 1: Create Deployment

```bash
kubectl create deployment backend-deployment --image=<your-docker-image>
```

Or using YAML:

```bash
kubectl apply -f k8s/

### Step 2: Verify Pods

```bash
kubectl get pods
```

Expected output:
```
NAME                                  READY   STATUS    RESTARTS   AGE
backend-deployment-xxxxx              1/1     Running   0          ...
```

Pod should be in:
```
STATUS = Running
```

---

## 🌐 Expose Service

### Option 1: NodePort

```bash
kubectl expose deployment backend-deployment \
  --type=NodePort \
  --port=5000
```

Get service details:

```bash
kubectl get svc
```

Access via:

```bash
minikube service backend-deployment
```

---

### Option 2: Port Forward (Recommended for local validation)

```bash
kubectl port-forward deployment/backend-deployment 8080:5000
```

Access in browser:

```
http://localhost:8080
```

---

## 🔍 Validate Pod Health

Check pod details:

```bash
kubectl describe pod <pod-name>
```

Check logs:

```bash
kubectl logs <pod-name>
```

No crash loops or errors should be present.

---

## 🧪 Validation Checklist

✔ Kubernetes cluster running locally  
✔ Node status = Ready  
✔ Deployment created successfully  
✔ Pods in Running state  
✔ No CrashLoopBackOff  
✔ Service accessible via port-forward / NodePort  
✔ Logs accessible  

---

## 🛑 Cluster Teardown

Stop cluster:

```bash
minikube stop
```

Delete cluster:

```bash
minikube delete
```

---

## 📊 Outcome Achieved

- Local Kubernetes cluster successfully installed and validated
- Containerized service deployed
- Pod health verified
- Service exposed and accessible
- Cluster startup & teardown documented
- Reproducible setup on fresh machine

---

## 🎯 Final Status

Minikube cluster validated successfully.

Local Kubernetes environment ready for
container orchestration and further CI/CD integration.
