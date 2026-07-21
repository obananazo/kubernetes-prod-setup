# Kubernetes Prod Setup

![CI](https://github.com/obananazo/kubernetes-prod-setup/actions/workflows/ci.yml/badge.svg)

A production-oriented local Kubernetes setup. Built to learn, reference, and reuse.

This is not a "hello world" throwaway. It reflects how real deployments are structured:

- containerized app
- environment configuration
- secrets management
- Helm-based packaging
- observability & monitoring via Prometheus + Grafana
- automated continuous integration & delivery
- Terraform code for infrastructure provisioning
- pre-commit hooks ensuring code style standards

---

## Stack

| Tool | Purpose |
| ---- | ------- |
| Python + Flask | Application |
| Docker | Containerization |
| Kubernetes | Orchestration |
| Helm | Package management |
| Minikube | Local cluster |
| GitHub Actions | CI/CD |
| Terraform (+ Ministack) | IaC *(coming soon)* |

---

## What this demonstrates

- Kubernetes `Deployment`, `Service`, `ConfigMap`, and `Secret` manifests
- Helm Chart with templated values for environment-specific configuration
- Liveness & readiness probes on `/health` endpoint
- Clean separation of app code, raw manifests, and Helm chart
- Local development workflow with Minikube
- Github Actions CI/CD
- Terraform IaC

---

## Project Structure

```sh
.
├── .github                 # Github Actions CI/CD
│   └── workflows
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml # Pre-commit hooks
├── Dockerfile              # Containerization
├── Makefile                # Automated workflows & command reference
├── README.md
├── app                     # Flask App with '/health' endpoint
│   ├── main.py
│   └── requirements.txt
├── helm-chart              # Helm templates
│   ├── Chart.yaml
│   ├── charts
│   ├── templates
│   │   ├── NOTES.txt
│   │   ├── _helpers.tpl
│   │   ├── configmap.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── tests
│   └── values.yaml
└── k8s                     # Kubernetes manifests
    ├── configmap.yaml
    ├── deployment.yaml
    ├── secret.yaml
    └── service.yaml
```

---

## Getting Started

### Prerequisites

```bash
brew install minikube kubectl helm
```

### Start the cluster

```bash
minikube start
eval $(minikube docker-env)
```

### Build the image

```bash
docker build -t k8s-prod-setup:latest .
```

### Deploy with Helm

```bash
helm install k8s-prod-setup k8s-prod-setup-chart/
```

### Access the app

```bash
minikube service k8s-prod-setup-k8s-prod-setup-chart --url
```

## Makefile

All common tasks are available via `make`:

| Command | Description |
| ------- | ----------- |
|`make`|Start cluster, build image, deploy — full setup|
|`make deploy`|Rebuild image and upgrade Helm release|
|`make open`|Get app URL|
|`make pods`|Show running pods|
|`make watch`|Watch pods live|
|`make logs`|Logs of first pod|
|`make logs <pod name>`|Logs of specific pod|
|`make restart`|Restart all pods|
|`make lint`|Lint Helm chart|
|`make rollback`|Rollback to previous Helm revision|
|`make clean`|Full teardown|

---

## Endpoints

| Endpoint | Description |
| -------- | ----------- |
| `/` | Returns app name and status |
| `/health` | Health check for liveness & readiness probes |

---

## Configuration

Environment variables are managed via Kubernetes ConfigMap and injected at runtime.
Secrets are base64-encoded in `k8s/secret.yaml`.

> ⚠️ Secrets in this repo are example values only.
> In production, secrets are managed via AWS Secrets Manager or HashiCorp Vault — never hardcoded in YAML.

---

## Roadmap

- [x] Basic containerized App
- [x] Kubernetes manifests
- [x] Secrets & Env management
- [x] Helm chart
- [x] Pre-commit hooks & linting
- [x] GitHub Actions CI/CD pipeline
- [ ] Ansible playbook for environment setup
- [ ] Prometheus + Grafana monitoring
- [ ] Terraform IaC + Ministack
