#!/bin/bash

set -e

echo "🚀 Starting full Transcept setup..."

# Step 1: Terraform Infrastructure
echo "🔧 Step 1: Setting up infrastructure with Terraform..."
cd infrastructure/terraform
terraform init
terraform apply -auto-approve
cd ../../..

# Step 2: Ansible Configuration
echo "🛠 Step 2: Configuring VMs with Ansible..."
cd infrastructure/ansible
ansible-playbook -i inventory.ini site.yml
cd ../../..

# Step 3: Deploying Kubernetes Resources
echo "☸️ Step 3: Deploying ArgoCD, Prometheus, and Grafana on Kubernetes..."
cd infrastructure/k8s
kubectl apply -f argocd-app.yaml
kubectl apply -f prometheus.yaml
kubectl apply -f grafana.yaml
cd ../../..

# Step 4: Model Training
echo "🤖 Step 4: Training Summarization and QA Models..."
cd model_training
python3 train_summarization.py
python3 train_qa.py
cd ..

# Step 5: Building & Pushing Docker Images
echo "🐳 Step 5: Building and pushing Docker images..."
cd model_serving/summarization_service
docker build -t summarizer .
# docker push your-docker-repo/summarizer  # Uncomment if pushing to DockerHub
cd ../qa_service
docker build -t qa-service .
# docker push your-docker-repo/qa-service  # Uncomment if pushing to DockerHub
cd ../../..

# Step 6: Deploying Summarization and QA APIs
echo "🌐 Step 6: Deploying Summarization and QA APIs to Kubernetes..."
kubectl apply -f infrastructure/k8s/summarization-service.yaml
kubectl apply -f infrastructure/k8s/qa-service.yaml

# Step 7: Running the Data Pipeline
echo "📡 Step 7: Simulating lecture uploads..."
cd data_pipeline
python3 simulate_stream.py
cd ..

echo "✅ Full Transcept setup complete!"
