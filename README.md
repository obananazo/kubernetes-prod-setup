# Kubernetes Prod Setup

![CI](https://github.com/obananazo/kubernetes-prod-setup/actions/workflows/ci.yml/badge.svg)

A production-oriented local Kubernetes setup. Built to learn, reference, and reuse.

It reflects how real deployments are structured:

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
| Python + Flask | Microservices |
| PostgreSQL | Database |
| Docker | Containerization |
| Kubernetes | Orchestration |
| Helm | Package management |
| Minikube | Local cluster |
| GitHub Actions | CI/CD |
| Prometheus | Metrics collection & scraping |
| Grafana | Visualization & dashboards |
| Terraform (+ Ministack) | IaC *(coming soon)* |

---

## What this demonstrates

A realistic microservices architecture (e-commerce example) running on Kubernetes that reflects how production deployments are structured.

- **Microservices** — independently deployable services with their own databases (User Service with PostgreSQL, JWT authentication)
- **Kubernetes primitives** — `Deployment`, `Service`, `ConfigMap`, `Secret`, `ServiceMonitor`
- **Helm** — templated, environment-specific deployments
- **Observability** — Prometheus metrics scraping + Grafana dashboards
- **CI/CD** — GitHub Actions pipeline with linting, formatting, and Docker build
- **Security** — secrets management, never hardcoded credentials
- **Developer experience** — Makefile workflows, pre-commit hooks, clean code standards

---

## Project Structure

```sh
.
├── .github
│   └── workflows               # Github Actions CI/CD
├── .gitignore
├── .pre-commit-config.yaml     # Pre-commit hooks
├── DECISIONS.md                # Info on chosen technologies
├── Makefile                    # Automated workflows & command reference
├── README.md
├── helm-chart                  # Helm templates
│   ├── Chart.yaml
│   ├── charts
│   ├── templates
│   └── values.yaml
├── k8s                         # Kubernetes manifests
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── secret.yaml
│   ├── service.yaml
│   └── servicemonitor.yaml
└── services                    # Microservices for e-commerce example
    └── user-service
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

> [!NOTE]
> If using MacOS (darwin) the terminal needs to be kept open (`make open`) in a separate terminal

### Monitoring

| Command | Description |
| ------- | ----------- |
|`make grafana`|Open Grafana in browser|
|`make grafana-pw`|Get Grafana admin password|
|`make prometheus`|Open Prometheus UI|

---

## Endpoints

| Endpoint | Description |
| -------- | ----------- |
| `/` | Returns app name and status |
| `/health` | Health check for liveness & readiness probes |
| `/metrics` | Used by Prometheus for scraping metrics |

---

## Configuration

Environment variables are managed via Kubernetes ConfigMap and injected at runtime.
Secrets are base64-encoded in `k8s/secret.yaml`.

> ⚠️ Secrets in this repo are example values only.
> In production, secrets are managed via AWS Secrets Manager or HashiCorp Vault — never hardcoded in YAML.

---

## Roadmap

- [x] ~~Basic containerized App~~ [Removed]
- [ ] E-commerce Demo/Microservices
    - [x] User service
    - [x] Product service
    - [ ] Order service
    - [ ] API Gateway
- [x] Pre-commit hooks & linting
- [x] GitHub Actions CI/CD pipeline
- [x] Kubernetes manifests
- [x] Helm chart
- [x] Secrets & Env management
- [ ] Prometheus + Grafana monitoring
- [ ] Ansible playbook for environment setup
- [ ] Terraform IaC + Ministack
