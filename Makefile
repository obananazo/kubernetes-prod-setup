# kubernetes-prod-setup
# Usage: make <target> — or just `make` to start everything

.PHONY: all start build install upgrade deploy restart open \
        stop clean lint template helm-status helm-history \
        rollback pods watch logs describe images status


# Global constants
IMAGE_NAME=k8s-prod-setup
HELM_RELEASE=k8s-prod-setup
HELM_CHART=helm-chart


# Default: start everything from scratch
all: start build install status

# Full rebuild and redeploy (build image + helm upgrade)
deploy: build upgrade
	kubectl get pods -w

# Full teardown
clean: uninstall stop


# --- Local Environment ---

# Start Minikube cluster
start:
	minikube start
	eval $$(minikube docker-env)

# Stop Minikube cluster
stop:
	minikube stop

# Get cluster & node status
status:
	minikube status
	kubectl get nodes
	kubectl get pods


# --- Docker ---

# Build Docker image inside Minikube's Docker context
build:
	eval $$(minikube docker-env) && docker build -t $(IMAGE_NAME):latest .

# List local images
images:
	docker images | grep $(IMAGE_NAME)


# --- Kubernetes ---

# Show running pods
pods:
	kubectl get pods

# Watch pods live
watch:
	kubectl get pods -w

# Show logs for a pod (usage: make logs POD=<pod-name>)
logs:
ifdef POD
	kubectl logs $(POD)
else
	kubectl logs $$(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep $(HELM_RELEASE) | head -1)
endif

## Describe a pod (usage: make describe POD=<pod-name>)
describe:
	kubectl describe pod $$(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep $(HELM_RELEASE) | head -1)

# Restart all pods in deployment
restart:
	kubectl rollout restart deployment


# --- Helm ---

# Install Helm release
install:
	helm install $(HELM_RELEASE) $(HELM_CHART)/

# Upgrade Helm release (use after code/config changes)
upgrade:
	helm upgrade $(HELM_RELEASE) $(HELM_CHART)/

# Uninstall Helm release
uninstall:
	helm uninstall $(HELM_RELEASE)

# Show Helm release status
helm-status:
	helm status $(HELM_RELEASE)

# Show Helm release history
helm-history:
	helm history $(HELM_RELEASE)

# Rollback to previous Helm revision
rollback:
	helm rollback $(HELM_RELEASE)

# Lint Helm chart
lint:
	helm lint $(HELM_CHART)/

# Render Helm templates locally (dry-run)
template:
	helm template $(HELM_CHART)/

# Open app URL in terminal
open:
	minikube service --url --namespace default $$(kubectl get svc --no-headers -o custom-columns=":metadata.name" | grep $(HELM_RELEASE))
