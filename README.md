# Kubernetes Prod Setup

[![Lint & build](https://github.com/obananazo/kubernetes-prod-setup/actions/workflows/lint-and-build.yml/badge.svg)](https://github.com/obananazo/kubernetes-prod-setup/actions/workflows/lint-and-build.yml) [![Validate manifests](https://github.com/obananazo/kubernetes-prod-setup/actions/workflows/validate-manifests.yml/badge.svg)](https://github.com/obananazo/kubernetes-prod-setup/actions/workflows/validate-manifests.yml)

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
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows               # Github Actions CI/CD
├── .gitignore
├── .pre-commit-config.yaml     # Pre-commit hooks
├── API.md                      # API endpoints reference
├── DECISIONS.md                # Info on chosen technologies
├── Makefile                    # Automated workflows & command reference
├── README.md
├── helm-chart                  # Helm templates
│   ├── .helmignore
│   ├── Chart.yaml
│   ├── charts
│   ├── templates
│   └── values.yaml
├── k8s                         # Cluster-wide K8s manifests
│   └── ingress.yaml
├── monitoring
│   └── dashboard.yaml          # Grafana dashboard
├── services                    # Microservices for e-commerce example
│   ├── order-service
│   ├── product-service
│   └── user-service
└── setup.cfg                   # Project-level config
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
```

### Deploy all services

```bash
# Create secrets
kubectl create secret generic user-service-secret \
  --from-literal=JWT_SECRET_KEY=change-me \
  --from-literal=POSTGRES_PASSWORD=change-me \
  --from-literal=POSTGRES_USER=postgres \
  --from-literal=DATABASE_URL=postgresql://postgres:change-me@user-postgres:5432/users

kubectl create secret generic product-service-secret \
  --from-literal=POSTGRES_PASSWORD=change-me \
  --from-literal=POSTGRES_USER=postgres \
  --from-literal=DATABASE_URL=postgresql://postgres:change-me@product-postgres:5432/products

kubectl create secret generic order-service-secret \
  --from-literal=POSTGRES_PASSWORD=change-me \
  --from-literal=POSTGRES_USER=postgres \
  --from-literal=DATABASE_URL=postgresql://postgres:change-me@order-postgres:5432/orders

# Build images
eval $(minikube docker-env)
docker build -t user-service:latest services/user-service/
docker build -t product-service:latest services/product-service/
docker build -t order-service:latest services/order-service/

# Deploy
kubectl apply -f services/user-service/k8s/
kubectl apply -f services/product-service/k8s/
kubectl apply -f services/order-service/k8s/

# Enable Ingress
minikube addons enable ingress
kubectl apply -f k8s/
```

### Access the services

```bash
# Start tunnel (keep open in separate terminal)
minikube tunnel

# Test endpoints
curl http://localhost/api/users/health
curl http://localhost/api/products/health
curl http://localhost/api/orders/health
```

## Makefile

> [!WARNING]
> Makefile commands are partially outdated — currently being updated for the microservices setup.

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

### Import the dashboard

1. Open Grafana (`make grafana`)
2. Go to **Dashboards → Import**
3. Upload `monitoring/dashboard.json` or paste its contents
4. Select **Prometheus** as the data source
5. Click **Import**

---

## Endpoints

See [API.md](API.md) for the full API reference.

---

## Configuration

Secrets are managed via Kubernetes Secrets, injected as environment variables at runtime.

> ⚠️ Secrets in this repo are example values only.
> In production, secrets are managed via AWS Secrets Manager or HashiCorp Vault — never hardcoded in YAML.

---

## Roadmap

- [x] ~~Basic containerized App~~ [Removed]
- [x] E-commerce Demo/Microservices
    - [x] User service
    - [x] Product service
    - [x] Order service
    - [x] API Gateway
- [x] Pre-commit hooks & linting
- [x] GitHub Actions CI/CD pipeline
- [x] Kubernetes manifests
- [x] Helm chart
- [x] Secrets & Env management
- [x] Prometheus + Grafana monitoring
- [ ] Terraform IaC + Ministack
- [ ] Ansible playbook for environment setup
