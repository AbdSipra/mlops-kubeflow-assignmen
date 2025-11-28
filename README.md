# MLOps Kubeflow Pipeline: Boston Housing Price Prediction

## 📋 Project Overview

This project implements a **production-ready MLOps pipeline** for predicting Boston housing prices using **Kubeflow Pipelines** (KFP) on **Minikube**, with **DVC** for data versioning and **MLflow** for experiment tracking. The pipeline demonstrates best practices in machine learning operations including data versioning, reproducible model training, metrics tracking, and CI/CD automation.

### Problem Statement
The project builds a **machine learning regression model** to predict Boston housing prices using the classic Boston Housing dataset. The pipeline automates the entire workflow from data extraction through model evaluation, making it reproducible and scalable.

### Key Technologies
- **Kubeflow Pipelines (KFP) v2.15.1**: Container-based ML orchestration
- **Minikube v1.37.0**: Local Kubernetes cluster for KFP deployment
- **DVC v3.x**: Data versioning and pipeline version control
- **MLflow v2.x**: Experiment tracking and model registry
- **GitHub Actions**: CI/CD automation for pipeline compilation
- **Python 3.10+**: Primary development language
- **scikit-learn**: ML model training (Random Forest)

### Project Structure

```
mlops-kubeflow-assignmen/
├── README.md                                 # This file - Project documentation
├── requirements.txt                          # Python dependencies
├── pipeline.py                               # Main KFP pipeline definition
├── compile_pipeline.py                       # Pipeline compilation script for CI/CD
├── Dockerfile                                # Container image for components
│
├── data/                                     # Data directory
│   ├── raw_data.csv                         # Boston Housing dataset (tracked with DVC)
│   └── raw_data.csv.dvc                     # DVC metadata file
│
├── src/                                      # Source code
│   ├── __init__.py                          
│   ├── pipeline_components.py               # 4 KFP component definitions
│   ├── model_training.py                    # Model training logic
│   ├── mlflow_pipeline.py                   # MLflow experiment tracking
│   └── __pycache__/
│
├── components/                               # Component YAML definitions (generated)
│   ├── data_extraction_component.yaml
│   ├── data_preprocessing_component.yaml
│   ├── model_training_component.yaml
│   └── model_evaluation_component.yaml
│
├── .github/                                  # CI/CD Configuration
│   └── workflows/
│       └── main.yml                         # GitHub Actions CI/CD workflow
│
├── mlruns/                                   # MLflow run artifacts and metrics
│   └── 0/                                   # Experiment tracking data
│
├── DELIVERABLE_1_DVC_SETUP.md              # Task 1: DVC setup documentation
├── DELIVERABLE_2_KFP_COMPONENTS.md         # Task 2: KFP components documentation
├── DELIVERABLE_3_KFP_DEPLOYMENT.md         # Task 3: KFP deployment documentation
├── DELIVERABLE_4_GITHUB_ACTIONS.md         # Task 4: GitHub Actions documentation
├── DELIVERABLE_4_QUICK_REFERENCE.md        # Task 4: Quick reference guide
├── GITHUB_ACTIONS_CONSOLE_GUIDE.md         # Task 4: Console output guide
└── pipeline.yaml                            # Compiled KFP pipeline (generated)
```

---

## 🚀 Setup Instructions

### Prerequisites
- **Windows 10/11** or Linux/macOS
- **Docker Desktop** installed and running
- **Git** for version control
- **Python 3.10 or higher**
- **kubectl** (installed with Minikube)

### 1. Install Minikube and Kubeflow Pipelines

#### Step 1.1: Install Minikube
```bash
# Download and install Minikube (Windows example)
# Visit: https://minikube.sigs.k8s.io/docs/start/

# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=50g
```

#### Step 1.2: Verify Kubernetes Cluster
```bash
# Check cluster status
minikube status

# Expected output:
# minikube: Running
# cluster: Running
# kubectl: Correctly Configured
```

#### Step 1.3: Install Kubeflow Pipelines

**Option A: Using kubectl apply (Recommended)**
```bash
# Deploy KFP to minikube
kubectl apply -k github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=2.0.0

# Wait for all pods to be ready (2-3 minutes)
kubectl wait --for=condition=ready pod -l app -n kubeflow --timeout=300s

# Deploy KFP within the kubeflow namespace
kubectl apply -k github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=2.0.0
```

**Option B: Using Minikube addon (Simpler)**
```bash
# Enable Kubeflow addon
minikube addons enable kubeflow

# Wait for deployment
kubectl wait --for=condition=ready pod -n kubeflow --all --timeout=600s
```

#### Step 1.4: Access Kubeflow UI
```bash
# Port-forward the KFP UI to localhost
minikube kubectl -- port-forward -n kubeflow svc/ml-pipeline-ui 8080:80 &

# Open browser and navigate to
# http://localhost:8080
```

### 2. Configure DVC (Data Versioning)

#### Step 2.1: Initialize DVC
```bash
# Install DVC (included in requirements.txt)
pip install dvc

# Initialize DVC in the repository
dvc init
```

#### Step 2.2: Configure Local DVC Remote Storage
```bash
# Create a local directory for DVC storage (e.g., /tmp/dvc-storage)
# Windows example:
mkdir C:\tmp\dvc-storage

# Configure as DVC remote
dvc remote add -d myremote C:\tmp\dvc-storage

# Verify remote configuration
dvc remote list
```

#### Step 2.3: Track Data with DVC
```bash
# Add data file to DVC
dvc add data/raw_data.csv

# Push data to remote storage
dvc push

# Verify data is tracked
git add data/raw_data.csv.dvc
git commit -m "Track data with DVC"
```

### 3. Set Up Python Environment

```bash
# Clone repository
git clone https://github.com/AbdSipra/mlops-kubeflow-assignmen
cd mlops-kubeflow-assignmen

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify KFP installation
python -c "import kfp; print(f'KFP Version: {kfp.__version__}')"
```

### 4. Configure MLflow (Optional: Experiment Tracking)

```bash
# MLflow is included in requirements.txt
# Start MLflow UI (runs on http://localhost:5000)
mlflow ui

# MLflow will track all experiments in ./mlruns directory
```

---

## 📊 Pipeline Walkthrough

### Pipeline Architecture

The pipeline consists of **4 connected components**:

```
Data Extraction
       ↓
Data Preprocessing
       ↓
Model Training
       ↓
Model Evaluation
```

### Component Details

#### 1️⃣ **Data Extraction Component**
```python
INPUT:  None (embedded Boston Housing dataset)
OUTPUT: raw_data.csv (features + target variable)
ACTION: Creates and outputs Boston Housing dataset (506 samples, 13 features)
```

**File:** `src/pipeline_components.py` (data_extraction_component)

#### 2️⃣ **Data Preprocessing Component**
```python
INPUT:  raw_data.csv from data extraction
OUTPUT: train_data.csv, test_data.csv
ACTION: 
  - Standardizes features using StandardScaler
  - Splits data: 80% train, 20% test
  - Handles missing values
  - Outputs CSV files for training
```

**File:** `src/pipeline_components.py` (data_preprocessing_component)

#### 3️⃣ **Model Training Component**
```python
INPUT:  train_data.csv from preprocessing
OUTPUT: model.joblib (trained Random Forest)
ACTION:
  - Trains Random Forest Regressor (100 trees)
  - Uses default hyperparameters
  - Serializes model with joblib
  - Outputs model.joblib for evaluation
```

**File:** `src/pipeline_components.py` (model_training_component)
**Model:** `src/model_training.py`

#### 4️⃣ **Model Evaluation Component**
```python
INPUT:  model.joblib (trained model)
        test_data.csv (test data)
OUTPUT: metrics.json (evaluation metrics)
ACTION:
  - Loads trained model
  - Generates predictions on test data
  - Calculates MSE (Mean Squared Error)
  - Calculates R² (Coefficient of Determination)
  - Outputs metrics to metrics.json
```

**File:** `src/pipeline_components.py` (model_evaluation_component)

### How to Compile the Pipeline

#### Method 1: Local Compilation (For Development)

```bash
# Navigate to project root
cd mlops-kubeflow-assignmen

# Run compilation script (includes validation)
python compile_pipeline.py

# Output: pipeline.yaml (KFP pipeline definition)
# Expected: 354 lines, ~15.6 KB
```

#### Method 2: Automatic Compilation (Via GitHub Actions)

When you push to GitHub main branch:

```bash
git add .
git commit -m "Update pipeline"
git push origin main
```

**GitHub Actions automatically:**
1. ✅ Checks out code
2. ✅ Sets up Python environment
3. ✅ Installs dependencies
4. ✅ Validates syntax
5. ✅ Compiles pipeline.yaml
6. ✅ Uploads artifacts (pipeline.yaml)

**View compilation results:**
- Go to: https://github.com/AbdSipra/mlops-kubeflow-assignmen/actions
- Click latest workflow run
- Check console output for compilation status

### How to Run the Pipeline on Kubeflow

#### Step 1: Ensure Minikube and KFP are Running
```bash
# Verify Minikube is running
minikube status

# Verify KFP pods are ready
kubectl get pods -n kubeflow | grep ml-pipeline
```

#### Step 2: Port-Forward KFP UI
```bash
# Open KFP UI on localhost:8080
minikube kubectl -- port-forward -n kubeflow svc/ml-pipeline-ui 8080:80 &
```

#### Step 3: Upload Pipeline to KFP UI
```bash
# Option A: Upload manually via KFP UI
# 1. Go to http://localhost:8080
# 2. Click "Upload pipeline"
# 3. Select pipeline.yaml from local disk
# 4. Click "Create"

# Option B: Upload via KFP SDK (Python)
python scripts/upload_pipeline.py
```

#### Step 4: Execute Pipeline
```bash
# Method A: Via KFP UI
# 1. Go to http://localhost:8080/pipelines
# 2. Click pipeline name
# 3. Click "Create run"
# 4. Set parameters and click "Start"

# Method B: Via CLI
kfp run create --pipeline-id <PIPELINE_ID> --run-name <RUN_NAME>
```

#### Step 5: Monitor Execution
```bash
# Watch component execution in real-time
# KFP UI shows:
# - Component status (Running/Success/Failed)
# - Execution timeline
# - Logs for each component
# - Output metrics and artifacts

# Expected execution time: 2-5 minutes
# Expected metrics (MSE ~7.9, R² ~0.89)
```

### Pipeline Execution Example

```
Pipeline Run: boston-housing-run-001
Status: ✅ SUCCESS (4m 32s)

Components Executed:
1. data_extraction_component ✅ (45s)
   Output: raw_data.csv (506 rows, 13 features)

2. data_preprocessing_component ✅ (38s)
   Output: train_data.csv, test_data.csv

3. model_training_component ✅ (2m 15s)
   Output: model.joblib (Random Forest, 100 trees)

4. model_evaluation_component ✅ (54s)
   Output: 
     - MSE: 7.927
     - R²: 0.892

Overall: Pipeline Successful ✅
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

### Workflow Overview

**Location:** `.github/workflows/main.yml`

**Triggered on:**
- Push to main branch
- Pull requests to main
- Manual workflow_dispatch

**What it does:**
1. **Environment Setup** - Installs dependencies
2. **Pipeline Compilation** - Compiles pipeline.py to pipeline.yaml
3. **Validation** - Verifies pipeline.yaml is valid

### Viewing CI/CD Execution

```bash
# URL: https://github.com/AbdSipra/mlops-kubeflow-assignmen/actions

# Steps:
# 1. Go to Actions tab
# 2. Click latest workflow run
# 3. Click "build-and-test" job
# 4. View console output for each stage

# Expected output:
# ✓ Set up Python 3.10
# ✓ Install dependencies
# ✓ Python syntax validation passed!
# ✓ Pipeline compiled successfully to pipeline.yaml
# ✓ pipeline.yaml verified: 354 lines, 15589 bytes
# ✓ CI/CD COMPILATION SUCCESSFUL!
```

### Deployment Artifacts

Each workflow run generates artifacts:
- `pipeline-yaml-py3.10` - Compiled pipeline (Python 3.10)
- `pipeline-yaml-py3.11` - Compiled pipeline (Python 3.11)
- `source-code-py3.10` - Source code snapshot

**Download artifacts:**
1. Go to Actions tab
2. Click workflow run
3. Scroll to "Artifacts" section
4. Download desired artifact

---

## 📈 MLflow Integration (Experiment Tracking)

### Starting MLflow UI
```bash
# Navigate to project root
cd mlops-kubeflow-assignmen

# Start MLflow UI (runs on http://localhost:5000)
mlflow ui

# View experiment tracking in browser
# http://localhost:5000
```

### What MLflow Tracks
- Model parameters (e.g., n_estimators=100)
- Metrics (e.g., MSE, R², RMSE)
- Artifacts (model files, data files)
- Git commit information
- Execution timestamps

### Viewing Experiments
```bash
# MLflow UI displays:
# - Experiment runs list
# - Comparison between runs
# - Parameter and metric charts
# - Artifact downloads
# - Git commit tracking
```

---

## 🐛 Troubleshooting

### Issue 1: Minikube Cluster Not Starting
```bash
# Solution: Increase allocated resources
minikube delete
minikube start --cpus=4 --memory=8192 --disk-size=50g

# Or check Docker Desktop is running
# Ensure virtualization is enabled in BIOS
```

### Issue 2: KFP UI Not Accessible
```bash
# Check if pods are running
kubectl get pods -n kubeflow

# Check service status
kubectl get svc -n kubeflow

# Port-forward again
minikube kubectl -- port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

### Issue 3: Pipeline Compilation Fails
```bash
# Verify syntax
python -m py_compile pipeline.py
python -m py_compile src/pipeline_components.py

# Check dependencies
pip list | grep kfp

# Run compilation script with verbose output
python compile_pipeline.py
```

### Issue 4: Data Extraction Component Fails
```bash
# Ensure data is available
ls -la data/raw_data.csv

# Verify DVC setup
dvc remote list

# Check git configuration
git config --list | grep dvc
```

### Issue 5: Model Evaluation Metrics Are Zero
```bash
# Verify test data exists
# Check model file is correctly serialized
# Ensure preprocessing split was successful

# Re-run pipeline
# Clear mlruns cache if needed
```

---

## 📚 Key Files Reference

| File | Purpose | Language |
|------|---------|----------|
| `pipeline.py` | Main KFP pipeline definition | Python |
| `src/pipeline_components.py` | 4 KFP component definitions | Python |
| `src/model_training.py` | Random Forest training logic | Python |
| `compile_pipeline.py` | Pipeline compilation script | Python |
| `.github/workflows/main.yml` | GitHub Actions CI/CD workflow | YAML |
| `requirements.txt` | Python dependencies | Text |
| `data/raw_data.csv` | Boston Housing dataset | CSV |

---

## 🔗 Important Links

**Repository:**
- GitHub: https://github.com/AbdSipra/mlops-kubeflow-assignmen

**Documentation:**
- Task 1 (DVC Setup): `DELIVERABLE_1_DVC_SETUP.md`
- Task 2 (KFP Components): `DELIVERABLE_2_KFP_COMPONENTS.md`
- Task 3 (KFP Deployment): `DELIVERABLE_3_KFP_DEPLOYMENT.md`
- Task 4 (GitHub Actions CI/CD): `DELIVERABLE_4_GITHUB_ACTIONS.md`
- Task 4 Quick Reference: `DELIVERABLE_4_QUICK_REFERENCE.md`

**External Resources:**
- Kubeflow Pipelines: https://www.kubeflow.org/docs/components/pipelines/
- KFP SDK: https://kubeflow-pipelines.readthedocs.io/
- Minikube: https://minikube.sigs.k8s.io/
- DVC: https://dvc.org/doc
- MLflow: https://mlflow.org/docs
- GitHub Actions: https://docs.github.com/en/actions

---

## 📋 Requirements

All dependencies are specified in `requirements.txt`:

```
dvc>=3.0.0              # Data versioning
pandas>=1.5.0           # Data manipulation
scikit-learn>=1.2.0     # Machine learning
kfp>=2.15.0             # Kubeflow Pipelines
numpy>=1.23.0           # Numerical computing
joblib>=1.2.0           # Model serialization
mlflow>=2.0.0           # Experiment tracking
```

**Install all requirements:**
```bash
pip install -r requirements.txt
```

---

## 🎯 Pipeline Workflow Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    MLOps Workflow Overview                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Development Cycle:                                              │
│  1. Edit pipeline.py or src/pipeline_components.py              │
│  2. Run: python compile_pipeline.py                             │
│  3. Review pipeline.yaml output                                 │
│  4. Commit and push to GitHub                                   │
│                                                                   │
│  CI/CD Automation (GitHub Actions):                              │
│  1. GitHub Actions triggered on push                            │
│  2. Python environment set up                                   │
│  3. Pipeline compiled automatically                             │
│  4. Artifacts stored for 30 days                                │
│                                                                   │
│  Production Deployment (Kubeflow):                               │
│  1. Upload pipeline.yaml to Kubeflow UI                         │
│  2. Create run with parameters                                  │
│  3. Monitor execution in real-time                              │
│  4. View metrics and artifacts                                  │
│  5. Track experiments in MLflow                                 │
│                                                                   │
│  Reproducibility (Data Versioning):                              │
│  1. Data tracked with DVC                                       │
│  2. Git tracks code and DVC metadata                            │
│  3. Any commit can be reproduced exactly                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 License

This project is part of an academic assignment for MLOps course.

---

## ✅ Checklist for Setup

- [ ] Minikube installed and running
- [ ] Kubeflow Pipelines deployed to Minikube
- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] DVC initialized and configured
- [ ] Data tracked with DVC
- [ ] Pipeline compiles successfully: `python compile_pipeline.py`
- [ ] GitHub repository cloned and up-to-date
- [ ] GitHub Actions workflow visible on Actions tab
- [ ] MLflow UI accessible on http://localhost:5000 (if running)
- [ ] KFP UI accessible on http://localhost:8080 (with port-forward)

---

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review specific task deliverables (DELIVERABLE_*.md files)
3. Check GitHub Actions console output for CI/CD issues
4. Review Kubeflow logs: `kubectl logs -n kubeflow <POD_NAME>`

---

**Last Updated:** November 28, 2025  
**Status:** ✅ Complete and Ready for Deployment
