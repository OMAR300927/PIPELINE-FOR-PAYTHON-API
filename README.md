# Python Demo Project: CI/CD Pipeline for Deploying Flask Application

This project simulates an AWS-like environment by using Docker Compose to build and deploy a Flask application with Docker, Jenkins, Gitleaks, Trivy, SonarQube, Kubernetes.

---

## Overview of the application

This project is a Flask-based web application built from scratch, designed to demonstrate a complete DevOps workflow including CI/CD, containerization, and deployment.

## Prerequisites

Make sure you have the following tools installed:

* Python & Flask
* Git and GitHub
* Docker & Docker Compose
* Gitleaks
* Trivy
* SonarQube
* Jenkins
* Kubernetes (Minikube)

---

## Steps in the CI/CD Pipeline

1. Get the Flask application.
2. Dockerize the backend of the Flask application.
3. Create a Docker Compose file to run Jenkins and SonarQube containers.
4. Create a Dockerfile for Jenkins to install the tools I need.
5. Push all Dockerfiles to the repository.
6. Go to SonarQube and create a token.
7. Use the token to create credentials in Jenkins and add the SonarQube server.
8. Write the Jenkinsfile.
9. Set up Kubernetes on a host using Minikube.
10. Create Kubernetes Deployment and Service for the backend.
11. Create Kubernetes PersistentVolume for SQLite DB.
12. Create Kubernetes Secret for the backend.
13. Use Jenkins to deploy the application to the Kubernetes cluster.

---

## Pipeline Steps

`Checkout --> Gitleaks scan --> SonarQube analysis --> Quality gate --> Scan file system --> Build & tag image --> Scan the image --> Push the image --> Apply Kubernetes manifests --> Verify the deployment`

---

## Project Structure

| File                      | Description |
|---------------------------|--------------------------------------------------------------|
| myapp/                    | Contains the application files and its Dockerfile            |
| K8s/                      | Contains Kubernetes manifests (cluster files)                |
| migrations/               | Database migration files                                     |
| Jenkinsfile               | Jenkins pipeline script                                      |
| Dockerfile                | Jenkins Dockerfile to install required tools                 |
| docker-compose-tools.yml  | Docker Compose file for Jenkins and SonarQube containers     |
| requirements.txt          | Contains the application dependencies                        |
| run.py                    | Used to run the application                                  |
| .env.example              | Contains the environment variables used in the application   |

---

## Conclusion

* I used this command to make the secret file:
```
kubectl create secret generic flask-secrets \
  --from-literal=FLASK_SQLALCHEMY_DATABASE_URI= \
  --from-literal=FLASK_JWT_SECRET_KEY= \
  --from-literal=FLASK_SECRET_KEY=
```

* After deploying the application, run `minikube service fr-service` to access it in the browser.

---

## Notes

* After running the cluster, you should go inside the Jenkins container and write the following commands:
1. export FLASK_APP=run.py
2. flask db upgrade
* I made these two steps manual, you can add this to the backend.yaml file as `initContainer`, or write it in the Jenkinsfile before `kubectl rollout`