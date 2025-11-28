# Task 3 Quick Start - Kubeflow Pipelines on Minikube

## What's Ready
✓ `pipeline.py` - Complete Kubeflow pipeline definition
✓ `pipeline.yaml` - Compiled pipeline (356 lines)
✓ All 4 components properly connected with data flow

## Step 1: Start Minikube (⏱️ ~2 minutes)
```powershell
minikube start --cpus=4 --memory=4096 --vm-driver=docker
```

Verify:
```powershell
minikube status
```

## Step 2: Deploy Kubeflow Pipelines (⏱️ ~3-5 minutes)

### Option A: Quick Deployment (Recommended)
```powershell
kubectl create namespace kubeflow
kubectl apply -k github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=master
kubectl apply -k github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=master

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=ml-pipeline -n kubeflow --timeout=300s
```

### Option B: Verify Deployment
```powershell
# Check if KFP pods are running
kubectl get pods -n kubeflow | grep ml-pipeline

# View pod logs if needed
kubectl logs -n kubeflow -l app=ml-pipeline
```

## Step 3: Access KFP Dashboard (⏱️ ~10 seconds)

### Terminal 1: Start Port Forward
```powershell
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

### Terminal 2: Open Browser
Open: **http://localhost:8080**

## Step 4: Upload & Run Pipeline (⏱️ ~5 minutes)

### Via Dashboard:
1. Click **Pipelines** (left menu)
2. Click **Upload a pipeline**
3. Select `pipeline.yaml` from your workspace
4. Enter name: **"Boston Housing ML Pipeline"**
5. Click **Create**
6. Click **Create Run**
7. Click **Start**
8. Monitor execution in real-time

### Via CLI (Alternative):
```powershell
# Install kfp client if needed
pip install kfp

# Upload and run
kfp run submit -e boston-housing-exp -p boston_housing_pipeline -f pipeline.yaml
```

## Expected Pipeline Graph
```
┌─────────────────────┐
│ Data Extraction     │
│ (dvc get)           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Data Preprocessing  │
│ (scale + split)     │
└──────────┬──────────┘
           │
           ├─────────────────┐
           │                 │
           ▼                 ▼
   ┌───────────────┐  ┌──────────────┐
   │  train.csv    │  │  test.csv    │
   └───────┬───────┘  └──────┬───────┘
           │                 │
           ▼                 │
┌─────────────────────┐      │
│ Model Training      │      │
│ (Random Forest)     │      │
└──────────┬──────────┘      │
           │                 │
           ▼                 ▼
┌─────────────────────────────────┐
│ Model Evaluation                │
│ (MSE, R² Score)                 │
└─────────────────────────────────┘
```

## Metrics to Expect
- **MSE**: ~25-30 (depending on dataset)
- **R² Score**: ~0.65-0.75

## Troubleshooting

### Port already in use
```powershell
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8081:80
# Then open: http://localhost:8081
```

### Pods not starting
```powershell
kubectl describe pod <pod-name> -n kubeflow
kubectl logs <pod-name> -n kubeflow
```

### Delete everything and restart
```powershell
minikube delete
minikube start --cpus=4 --memory=4096 --vm-driver=docker
# Then re-deploy
```

## Task 3 Deliverables Checklist
- [ ] Screenshot of `minikube status` (all services running)
- [ ] Screenshot of KFP UI showing pipeline graph with 4 connected steps
- [ ] Screenshot of run details showing metrics (MSE, R² Score)
- [ ] Copy of `pipeline.yaml` in repo

## Next: Task 4
After completing Task 3:
- Task 4 requires setting up Jenkins or GitHub Workflows
- You'll need a Jenkinsfile for CI/CD
- See `TASK3_SETUP_GUIDE.md` for detailed Minikube setup

---

**Total Time: ~10-15 minutes** ⏱️
