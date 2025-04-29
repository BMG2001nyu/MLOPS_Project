# Transcept: LoRA Fine-Tuned Summarization and QA for Lecture Transcripts

## 🧠 Overview
Transcept is a complete MLOps system designed for LMS platforms like Canvas or Moodle. It:
- Transcribes lecture audio/video using Whisper ASR
- Summarizes lectures using LoRA-tuned Mistral-7B
- Answers student questions using LoRA-tuned Phi-3.5 Mini

## 🚀 Features
- Fully containerized (Docker + Kubernetes)
- CI/CD with GitHub Actions + ArgoCD
- Canary deployments + automated rollback (Argo Rollouts)
- Prometheus + Grafana monitoring
- MLflow experiment tracking
- Runs on Chameleon Cloud infrastructure

---

## 🛠️ Setup Guide

### Step 1: Chameleon Cloud Infrastructure
- Provision:
  - 1x m1.medium (API/orchestration)
  - 2x GPU VMs (A100, for fine-tuning)
  - 50GB Persistent Volume
  - 1x Floating IP (for API/monitoring access)

### Step 2: Infrastructure as Code
```bash
cd infrastructure/terraform
terraform init && terraform apply
