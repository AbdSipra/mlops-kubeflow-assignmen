# Task 3: Kubeflow Pipelines on Minikube - Setup Guide

## Prerequisites
- Docker installed and running
- 4+ GB RAM available
- Windows PowerShell

## Step 1: Install Minikube

### Download and Install Minikube
```powershell
# Download Minikube installer
Invoke-WebRequest -Uri "https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe" -OutFile "$env:TEMP\minikube-installer.exe"

# Run installer
& "$env:TEMP\minikube-installer.exe"
```

Or use Chocolatey (if installed):
```powershell
choco install minikube
```

### Install kubectl
```powershell
choco install kubernetes-cli
```

Or download directly:
```powershell
Invoke-WebRequest -Uri "https://dl.k8s.io/release/stable.txt" -OutFile "$env:TEMP\version.txt"
$version = Get-Content "$env:TEMP\version.txt"
Invoke-WebRequest -Uri "https://dl.k8s.io/release/$version/bin/windows/amd64/kubectl.exe" -OutFile "C:\Program Files\kubectl.exe"
```

---

## Step 2: Start Minikube

```powershell
# Start Minikube cluster (allocate resources)
minikube start --cpus=4 --memory=4096 --vm-driver=docker

# Verify cluster is running
minikube status

# Get cluster info
kubectl cluster-info
```

Expected output for `minikube status`:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

---

## Step 3: Deploy Kubeflow Pipelines

### Option A: Standalone KFP Installation (Recommended for Learning)

```powershell
# Create kfp namespace
kubectl create namespace kfp

# Install KFP standalone
kubectl apply -k github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=master
kubectl apply -k github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=master

# Wait for deployment (may take 2-3 minutes)
kubectl wait --for=condition=ready pod -l app=ml-pipeline -n kubeflow --timeout=300s
```

### Option B: Using Kubeflow Manifests

```powershell
# Clone Kubeflow manifests
git clone https://github.com/kubeflow/manifests.git
cd manifests

# Deploy Kubeflow (full installation)
kustomize build example | kubectl apply -f -
```

---

## Step 4: Access Kubeflow Pipelines Dashboard

### Port Forward to Local Machine
```powershell
# Forward port 8080 to access KFP UI
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80

# Alternative: if kubeflow namespace is used
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 3000:80
```

### Open in Browser
Open: **http://localhost:8080** or **http://localhost:3000**

---

## Step 5: Compile and Upload Pipeline

### Compile Pipeline YAML
```powershell
cd C:\Users\abdul\Desktop\mlops-kubeflow-assignmen

# Run pipeline compilation
python pipeline.py

# Verify pipeline.yaml was created
Get-Item pipeline.yaml
```

### Upload to KFP Dashboard
1. Open http://localhost:8080 in browser
2. Click **"Pipelines"** on the left
3. Click **"Upload a pipeline"**
4. Select `pipeline.yaml` from your workspace
5. Fill in pipeline name: **"Boston Housing ML Pipeline"**
6. Click **"Create"**

---

## Step 6: Create and Run a Pipeline Experiment

1. Go to **Experiments** in KFP UI
2. Click **"Create experiment"**
3. Enter name: **"boston-housing-exp"**
4. Select the uploaded pipeline
5. Set parameters (or use defaults):
   - `dvc_repo_url`: https://github.com/AbdSipra/mlops-kubeflow-assignmen
   - `dvc_data_path`: data/raw_data.csv
6. Click **"Run"**
7. Monitor the pipeline execution in the dashboard

---

## Useful Commands

```powershell
# Check Minikube status
minikube status

# View running pods
kubectl get pods -n kubeflow

# View pod logs
kubectl logs -n kubeflow <pod-name>

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete

# SSH into Minikube
minikube ssh

# View services
kubectl get svc -n kubeflow

# Port forward with verbose output
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80 -v=4
```

---

## Troubleshooting

### "Connection refused" when accessing http://localhost:8080
- Ensure port-forward is still running in terminal
- Check if pods are ready: `kubectl get pods -n kubeflow`
- Restart port-forward if needed

### Pod stuck in "Pending" state
```powershell
# Check pod events
kubectl describe pod <pod-name> -n kubeflow

# Check node resources
kubectl top nodes
```

### Minikube won't start
```powershell
# Delete and restart fresh
minikube delete
minikube start --cpus=4 --memory=4096 --vm-driver=docker
```

### Permission denied errors
Run PowerShell as **Administrator**

---

## Verifying Task 3 Completion

After successful deployment, you should have:
✓ Minikube cluster running (`minikube status` shows all Running)
✓ Kubeflow Pipelines UI accessible at http://localhost:8080
✓ Pipeline uploaded and compiled
✓ Pipeline run completed successfully with all 4 steps visible:
  1. Data Extraction
  2. Data Preprocessing
  3. Model Training
  4. Model Evaluation
✓ Metrics and artifacts visible in the run details

---

## Next Steps

- Take screenshots of:
  - `minikube status` output
  - Kubeflow Pipelines dashboard with pipeline graph
  - Pipeline run details showing metrics
- These are your Task 3 deliverables!
