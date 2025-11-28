# Task 3 Deliverables Guide

## Overview
Task 3 requires demonstrating a Kubeflow Pipeline running on Minikube. Below is what you need to capture and submit.

## Required Deliverables

### 1️⃣ Minikube Status Screenshot
**Command:**
```powershell
minikube status
```

**Expected Output:**
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

**What to Capture**: Full terminal showing all statuses = "Running"

---

### 2️⃣ Kubeflow Pipelines Dashboard Screenshots

#### 2a. Pipeline Graph View
**How to get there:**
1. Open http://localhost:8080
2. Click **Pipelines** (left menu)
3. Click your pipeline name
4. Click **Graph** tab

**What to Capture**:
- All 4 components visible and connected:
  - Data Extraction
  - Data Preprocessing  
  - Model Training
  - Model Evaluation
- Clear arrows showing data flow between components

#### 2b. Pipeline Run Status
**How to get there:**
1. In KFP UI, click **Runs** (left menu)
2. Click on your completed run
3. Scroll to see the graph with status badges

**What to Capture**:
- All 4 steps showing ✅ **Completed** status
- Component names clearly visible
- Timeline/duration if available

#### 2c. Run Details with Metrics
**How to get there:**
1. In the Run view, scroll down or click a component
2. Look for **Metrics** or **Outputs** section
3. Find the evaluation component output

**What to Capture**:
```
Metrics:
- mse: [value]
- r2_score: [value]
```

---

### 3️⃣ KFP Dashboard Pod Logs (Optional but Helpful)

**Command to get pod details:**
```powershell
kubectl get pods -n kubeflow
kubectl logs <ml-pipeline-pod-name> -n kubeflow
```

**What to Show**: Terminal showing pod logs with successful execution

---

## How to Collect Screenshots

### Method 1: Windows Built-in
- Press **Windows + Shift + S** to open Snip & Sketch
- Capture area
- Save as PNG

### Method 2: PowerShell Screenshot
```powershell
Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save("C:\screenshot.png")
$graphics.Dispose()
$bitmap.Dispose()
```

### Method 3: Browser Developer Tools
- F12 → Device Toolbar → Take Screenshot

---

## Deliverable Submission Checklist

- [ ] Screenshot 1: `minikube status` - All services Running
- [ ] Screenshot 2: KFP Pipeline graph - 4 components connected
- [ ] Screenshot 3: Pipeline run - All steps Completed
- [ ] Screenshot 4: Evaluation metrics - MSE and R² Score values visible
- [ ] File: `pipeline.yaml` - In repository root
- [ ] File: `pipeline.py` - Shows `@dsl.pipeline` decorator
- [ ] File: `src/pipeline_components.py` - Shows all 4 components

---

## Example Expected Values

Your pipeline should produce metrics like:
```
MSE: ~20-30 (Mean Squared Error)
R² Score: ~0.65-0.75 (R-squared coefficient)
```

Exact values depend on train/test split randomness, but should be in this range.

---

## Troubleshooting Before Submission

### "Pipeline shows failed/error status"
```powershell
# Check pod logs
kubectl logs -n kubeflow <failed-pod-name>

# Common issues:
# 1. DVC data not found - verify dvc_repo_url parameter
# 2. Out of memory - increase Minikube memory: minikube delete && minikube start --memory=6144
# 3. Permissions - run PowerShell as Administrator
```

### "Can't see metrics"
- Click on the **Evaluation** component in the graph
- In right panel, expand **Outputs** or **Metrics** section
- Metrics are in `/tmp/metrics.json` artifact

### "Pipeline takes too long"
- First run may take 5-10 minutes (downloading images, initializing)
- Subsequent runs should be faster (~2-3 minutes)
- Check pod status: `kubectl get pods -n kubeflow`

---

## File Locations for Submission

```
mlops-kubeflow-assignmen/
├── pipeline.py                    ← Show this: @dsl.pipeline definition
├── pipeline.yaml                  ← Include this: compiled pipeline
├── src/
│   └── pipeline_components.py     ← Show this: all 4 components
├── components/                    ← YAML files: auto-generated
├── TASK3_IMPLEMENTATION.md        ← Reference document
└── QUICK_START_TASK3.md          ← Reference guide
```

---

## What Graders Will Look For

✓ **Minikube running** - `minikube status` shows all Running
✓ **Kubeflow deployed** - KFP UI accessible at http://localhost:8080
✓ **Pipeline connected** - 4 components with proper data flow
✓ **All steps complete** - No failed or error status
✓ **Metrics calculated** - MSE and R² Score values logged
✓ **Code quality** - Clean pipeline definition with proper decorators
✓ **Documentation** - Code is readable with comments

---

## Summary

| Deliverable | Location | How to Get |
|---|---|---|
| Screenshot: minikube status | Terminal | `minikube status` |
| Screenshot: KFP graph | Browser | http://localhost:8080 → Pipelines → Your pipeline → Graph |
| Screenshot: Run status | Browser | http://localhost:8080 → Runs → Your run |
| Screenshot: Metrics | Browser | KFP UI → Your run → Evaluation component → Outputs |
| File: pipeline.yaml | Repo root | Auto-generated from `pipeline.py` |
| File: pipeline.py | Repo root | Shows 4 connected components |
| File: pipeline_components.py | src/ | All 4 component definitions |

---

**Ready to submit Task 3!** ✅

Once you have all screenshots and files, you're ready for Task 4 (Jenkins CI/CD).
