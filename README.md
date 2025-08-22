


# Person App - Kubernetes Demo

This project is a simple **person data management web app** deployed on **Kubernetes**.  
It consists of a **frontend**, **backend**, and **PostgreSQL database**, all running as Kubernetes pods.

---

## Prerequisites

- Docker
- Minikube (or any Kubernetes cluster)
- kubectl
- Python 3.12 (for backend)
- Node.js (if you want to run frontend locally)

---

## Setup and Run Locally

### Backend

1. Go to backend folder:

```bash
cd backend
```

2. Install dependencies:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

3. Start backend:

```bash
python app.py
```

---

### Frontend

1. Go to frontend folder:

```bash
cd frontend
```

2. Start frontend using a live server or Node.js:

```bash
# Using live server extension or http-server
npx http-server -p 5000
```

3. Open `http://localhost:5000` in your browser.

---

## Docker Build

Make sure Docker is pointing to Minikube (optional):

```bash
eval $(minikube docker-env)
```

### Backend image

```bash
docker build -t person-backend:latest ./backend
```

### Frontend image

```bash
docker build -t person-frontend:latest ./frontend
```

---

## Kubernetes Deployment

1. Apply all YAMLs:

```bash
kubectl apply -f k8s/
```

2. Check pods and services:

```bash
kubectl get pods
kubectl get svc
```

3. Access frontend:

```bash
kubectl port-forward svc/frontend-service 3000:80
```

* Open in browser: `http://localhost:3000`

4. Backend API can be tested via port-forward:

```bash
kubectl port-forward svc/backend-service 5000:5000
curl http://localhost:5000/persons
```

---

## Notes

* Frontend must point to backend correctly:

  * **Inside cluster:** `http://backend-service:5000`
  * **From host with port-forward:** `http://localhost:5000`
* PostgreSQL data is stored in a **StatefulSet** with persistent volume, so data is retained even if pod restarts.
* Use `.env` files for sensitive credentials and **do not commit them**.

---

## Clean Up

Remove all deployments, services, and pods:

```bash
kubectl delete -f k8s/
```

Or scale deployments to zero:

```bash
kubectl scale deployment person-backend --replicas=0
kubectl scale deployment person-frontend --replicas=0
kubectl scale statefulset person-postgres --replicas=0
```

Or scale deployments back to one to restart:

```bash
kubectl scale deployment person-backend --replicas=1
kubectl scale deployment person-frontend --replicas=1
kubectl scale statefulset person-postgres --replicas=1
```


