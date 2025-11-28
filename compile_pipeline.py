#!/usr/bin/env python3
"""
Compile the Kubeflow pipeline from pipeline.py to pipeline.yaml
This script is used by GitHub Actions CI/CD
"""
import sys
import os
import subprocess

# Change to the repo directory
repo_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(repo_dir)

# Ensure components directory exists
os.makedirs("components", exist_ok=True)

try:
    # Step 1: Validate Python syntax
    print("Step 1: Validating Python syntax...")
    subprocess.run(
        [sys.executable, "-m", "py_compile", "src/pipeline_components.py"], check=True
    )
    subprocess.run([sys.executable, "-m", "py_compile", "pipeline.py"], check=True)
    print("✓ Python syntax validation passed!")

    # Step 2: Run pipeline.py to compile
    print("\nStep 2: Compiling pipeline to YAML...")
    subprocess.run([sys.executable, "pipeline.py"], check=True)

    # Step 3: Verify output
    print("\nStep 3: Verifying output...")
    if os.path.exists("pipeline.yaml"):
        file_size = os.path.getsize("pipeline.yaml")
        with open("pipeline.yaml", "r") as f:
            lines = len(f.readlines())
        print(f"✓ pipeline.yaml verified: {lines} lines, {file_size} bytes")
        print("\n" + "=" * 50)
        print("✓ CI/CD COMPILATION SUCCESSFUL!")
        print("=" * 50)
    else:
        print("✗ ERROR: pipeline.yaml was not generated!")
        sys.exit(1)

except subprocess.CalledProcessError as e:
    print(f"✗ ERROR: Subprocess failed with exit code {e.returncode}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
