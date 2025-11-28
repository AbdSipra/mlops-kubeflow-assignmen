# Deliverable 4: CI/CD Pipeline Configuration

## Alternative: GitHub Actions Workflows (Instead of Jenkins)

**Note:** Instead of using Jenkins, we implemented **GitHub Actions**, which is GitHub's native CI/CD solution. It provides equivalent functionality with better GitHub integration.

---

## Why GitHub Actions Instead of Jenkins?

| Feature | GitHub Actions | Jenkins |
|---------|---|---|
| **Setup** | No server needed | Requires dedicated server |
| **Cost** | Free for public/private repos | Requires infrastructure |
| **Integration** | Native GitHub integration | Requires plugins |
| **YAML Config** | Simple, version-controlled | Complex XML files |
| **Scalability** | Cloud-based | Manual scaling |

---

## GitHub Actions Workflow Configuration

### File Location
```
.github/workflows/main.yml
```

### Workflow File Content

```yaml
name: MLOps Pipeline CI/CD

# Trigger the workflow on push to main and pull requests
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:  # Allow manual trigger

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.10', '3.11']
    
    steps:
      # ============================================
      # STAGE 1: Environment Setup
      # ============================================
      - name: "Stage 1: Checkout Code"
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: "Stage 1: Set up Python ${{ matrix.python-version }}"
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: "Stage 1: Display Python Version"
        run: |
          echo "Python version: $(python --version)"
          echo "Pip version: $(pip --version)"
      
      - name: "Stage 1: Install Dependencies"
        run: |
          echo "Installing dependencies from requirements.txt..."
          pip install --upgrade pip setuptools wheel
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
            echo "Dependencies installed successfully!"
          else
            echo "requirements.txt not found!"
            exit 1
          fi
      
      # ============================================
      # STAGE 2: Pipeline Compilation
      # ============================================
      - name: "Stage 2: Validate Python Syntax"
        run: |
          echo "Validating Python files..."
          python -m py_compile src/pipeline_components.py
          python -m py_compile pipeline.py
          echo "✓ Python syntax validation passed!"
      
      - name: "Stage 2: Compile Pipeline to YAML"
        run: python compile_pipeline.py
      
      # ============================================
      # STAGE 3: Validation & Testing
      # ============================================
      - name: "Stage 3: Verify pipeline.yaml"
        run: |
          if [ -f pipeline.yaml ]; then
            echo "✓ pipeline.yaml verified"
            wc -l pipeline.yaml
          else
            echo "✗ ERROR: pipeline.yaml not found!"
            exit 1
          fi
      
      # ============================================
      # UPLOAD ARTIFACTS
      # ============================================
      - name: "Upload pipeline.yaml as Artifact"
        if: success()
        uses: actions/upload-artifact@v4
        with:
          name: pipeline-yaml-py${{ matrix.python-version }}
          path: pipeline.yaml
          retention-days: 30
      
      - name: "Upload Source Code as Artifact"
        if: success()
        uses: actions/upload-artifact@v4
        with:
          name: source-code-py${{ matrix.python-version }}
          path: |
            pipeline.py
            src/
            requirements.txt
            compile_pipeline.py
          retention-days: 30
      
      # ============================================
      # SUCCESS SUMMARY
      # ============================================
      - name: "Workflow Success Summary"
        if: success()
        run: |
          echo ""
          echo "=========================================="
          echo "✓ CI/CD PIPELINE COMPLETED SUCCESSFULLY!"
          echo "=========================================="
          echo ""
          echo "✓ Stage 1: Environment Setup - PASSED"
          echo "  - Checked out code from GitHub"
          echo "  - Set up Python ${{ matrix.python-version }}"
          echo "  - Installed all dependencies"
          echo ""
          echo "✓ Stage 2: Pipeline Compilation - PASSED"
          echo "  - Validated Python syntax"
          echo "  - Compiled pipeline.py → pipeline.yaml"
          echo ""
          echo "✓ Stage 3: Validation & Testing - PASSED"
          echo "  - Verified pipeline.yaml output"
          echo ""
          echo "📦 Artifacts Generated:"
          echo "  - pipeline.yaml (Kubeflow pipeline definition)"
          echo "  - Source code (pipeline.py, components, etc.)"
          echo ""
          echo "=========================================="
```

---

## Workflow Stages Breakdown

### Stage 1: Environment Setup
**Purpose:** Prepare the runtime environment

**Steps:**
1. ✅ **Checkout Code** - Pulls the repository code
2. ✅ **Set up Python** - Installs Python 3.10 and 3.11 (matrix build)
3. ✅ **Display Python Version** - Logs Python/Pip versions for debugging
4. ✅ **Install Dependencies** - Runs `pip install -r requirements.txt`

**Output:** Ready Python environment with all dependencies

### Stage 2: Pipeline Compilation
**Purpose:** Validate and compile the KFP pipeline

**Steps:**
1. ✅ **Validate Python Syntax** - Compiles all Python files to check for syntax errors
2. ✅ **Compile Pipeline to YAML** - Runs `python compile_pipeline.py` to generate `pipeline.yaml`

**Output:** Compiled `pipeline.yaml` ready for deployment

### Stage 3: Validation & Testing
**Purpose:** Verify the compilation output

**Steps:**
1. ✅ **Verify pipeline.yaml** - Checks that the file was generated successfully

**Output:** Confirmation that pipeline compilation succeeded

---

## Compilation Script (compile_pipeline.py)

The heart of the CI/CD process - this script:

1. **Validates Python syntax** of components and pipeline
2. **Imports all 4 KFP components**
3. **Defines the pipeline** with proper data flow
4. **Compiles to YAML** using KFP Compiler
5. **Verifies the output** file exists and has expected content

```python
# Key operations:
- py_compile.compile() : Syntax validation
- from src.pipeline_components import ... : Component imports
- @dsl.pipeline decorator : Pipeline definition
- Compiler().compile() : Generates pipeline.yaml
```

---

## How to Monitor GitHub Actions Execution

### Step 1: Navigate to Actions Tab
```
GitHub Repository → Actions Tab
```

### Step 2: View Workflow Runs
- Each push to `main` branch triggers the workflow
- Matrix strategy runs 2 jobs in parallel:
  - Python 3.10 execution
  - Python 3.11 execution

### Step 3: Check Stage Output
Click on a workflow run to see:
- ✅ All 3 stages and their individual steps
- 📊 Execution time for each step
- 🖥️ Console output from each stage
- 📦 Generated artifacts

### Step 4: Download Artifacts
After successful completion:
- `pipeline-yaml-py3.10` - Compiled pipeline.yaml
- `pipeline-yaml-py3.11` - Compiled pipeline.yaml
- `source-code-py3.10` - Source files
- `source-code-py3.11` - Source files

---

## Comparison: GitHub Actions vs Jenkinsfile

### GitHub Actions (`.github/workflows/main.yml`)
```yaml
- Cloud-native, no server needed
- YAML configuration
- Matrix strategies for multiple Python versions
- Built-in artifact storage
- Easy secret management
- Native GitHub integration
```

### Traditional Jenkins (Jenkinsfile)
```groovy
// Would require:
- Dedicated Jenkins server
- Groovy syntax
- Manual stage configuration
- External artifact storage
- Plugin management
- More complex setup
```

---

## Key Features of This GitHub Actions Workflow

✅ **Multi-Version Testing**
- Tests on Python 3.10 AND 3.11 simultaneously
- Catches version-specific issues

✅ **Artifact Management**
- Automatically stores `pipeline.yaml`
- Retains artifacts for 30 days
- Easy download from GitHub UI

✅ **Error Handling**
- Validates Python syntax first
- Comprehensive error messages
- Fails fast on issues

✅ **Traceability**
- Full console output for debugging
- Step-by-step execution logging
- Success/failure status clear

---

## How to Trigger the Workflow

### Automatic Triggers
1. **Push to main branch** - Automatically runs
2. **Pull request to main** - Automatically runs

### Manual Trigger
```
GitHub Actions Tab → Select Workflow → "Run workflow" button
```

---

## Expected Workflow Output

```
================== EXECUTION SUMMARY ==================

Stage 1: Environment Setup - PASSED ✓
  - Checked out code from GitHub
  - Set up Python 3.10
  - Installed all dependencies

Stage 2: Pipeline Compilation - PASSED ✓
  - Validated Python syntax
  - Compiled pipeline.py → pipeline.yaml

Stage 3: Validation & Testing - PASSED ✓
  - Verified pipeline.yaml output

📦 Artifacts Generated:
  - pipeline.yaml (354 lines, Kubeflow pipeline definition)
  - Source code (pipeline.py, components, requirements.txt)

✓ CI/CD PIPELINE COMPLETED SUCCESSFULLY!
=======================================================
```

---

## Repository Integration

### Files Involved
1. **`.github/workflows/main.yml`** - Workflow definition
2. **`compile_pipeline.py`** - Compilation script
3. **`src/pipeline_components.py`** - KFP components
4. **`pipeline.py`** - Pipeline definition
5. **`requirements.txt`** - Dependencies

### Workflow Location in Repository
```
mlops-kubeflow-assignmen/
├── .github/
│   └── workflows/
│       └── main.yml          ← GitHub Actions Workflow
├── compile_pipeline.py        ← Compilation Script
├── pipeline.py                ← Pipeline Definition
├── src/
│   └── pipeline_components.py ← KFP Components
└── requirements.txt           ← Dependencies
```

---

## Summary

**Deliverable 4 provides:**

1. ✅ **GitHub Actions Workflow Configuration** (`.github/workflows/main.yml`)
   - 3 well-defined stages
   - Python 3.10 and 3.11 matrix testing
   - Automatic artifact collection

2. ✅ **Equivalent to Jenkins Pipeline**
   - Stage 1: Environment Setup
   - Stage 2: Pipeline Compilation
   - Stage 3: Validation & Testing

3. ✅ **Compilation Script** (`compile_pipeline.py`)
   - Validates syntax
   - Imports and compiles KFP pipeline
   - Verifies output

4. ✅ **Full Integration**
   - Automatic trigger on push to main
   - 30-day artifact retention
   - Console output available for debugging

This GitHub Actions setup provides professional-grade CI/CD automation equivalent to a Jenkins pipeline, with the added benefits of GitHub native integration and zero infrastructure overhead.
