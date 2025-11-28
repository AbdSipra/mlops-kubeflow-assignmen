#!/usr/bin/env python3
"""
Compile the Kubeflow pipeline from pipeline.py to pipeline.yaml
This script is used by GitHub Actions CI/CD
"""
import sys
import os

# Change to the repo directory
repo_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(repo_dir)

# Ensure components directory exists
os.makedirs("components", exist_ok=True)

try:
    # Step 1: Validate Python syntax
    print("Step 1: Validating Python syntax...")
    import py_compile

    py_compile.compile("src/pipeline_components.py", doraise=True)
    py_compile.compile("pipeline.py", doraise=True)
    print("✓ Python syntax validation passed!")

    # Step 2: Import and compile directly
    print("\nStep 2: Compiling pipeline to YAML...")
    sys.path.insert(0, repo_dir)

    from kfp import dsl, compiler
    from src.pipeline_components import (
        data_extraction_component,
        data_preprocessing_component,
        model_training_component,
        model_evaluation_component,
    )

    @dsl.pipeline(
        name="Boston Housing ML Pipeline",
        description="End-to-end ML pipeline: data extraction -> preprocessing -> training -> evaluation",
    )
    def boston_housing_pipeline(
        dvc_repo_url: str = "https://github.com/AbdSipra/mlops-kubeflow-assignmen",
        dvc_data_path: str = "data/raw_data.csv",
    ):
        data_extraction_task = data_extraction_component(
            dvc_repo_url=dvc_repo_url,
            dvc_data_path=dvc_data_path,
            output_csv_path="/tmp/raw_data.csv",
        ).set_display_name("Data Extraction")

        preprocessing_task = data_preprocessing_component(
            raw_csv_path=data_extraction_task.output,
            train_csv_path="/tmp/train.csv",
            test_csv_path="/tmp/test.csv",
            test_size=0.2,
            random_state=42,
        ).set_display_name("Data Preprocessing")

        training_task = model_training_component(
            train_csv_path=preprocessing_task.output,
            model_output_path="/tmp/model.joblib",
            n_estimators=100,
            random_state=42,
        ).set_display_name("Model Training")

        evaluation_task = model_evaluation_component(
            model_path=training_task.output,
            test_csv_path="/tmp/test.csv",
            metrics_output_path="/tmp/metrics.json",
        ).set_display_name("Model Evaluation")

    compiler.Compiler().compile(
        pipeline_func=boston_housing_pipeline,
        package_path="pipeline.yaml",
    )
    print("✓ Pipeline compiled successfully to pipeline.yaml")

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

except Exception as e:
    print(f"✗ ERROR: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
