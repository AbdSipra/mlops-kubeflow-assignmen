#!/usr/bin/env python3
"""
Compile the Kubeflow pipeline from pipeline.py to pipeline.yaml
This script is used by GitHub Actions CI/CD
"""
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.pipeline_components import (
        data_extraction_component,
        data_preprocessing_component,
        model_training_component,
        model_evaluation_component
    )
    from kfp.compiler import Compiler
    import kfp.dsl as dsl
    
    print("✓ All imports successful")
    
    # Define the pipeline
    @dsl.pipeline(
        name='Boston Housing ML Pipeline',
        description='End-to-end ML pipeline: data extraction -> preprocessing -> training -> evaluation'
    )
    def boston_housing_pipeline(
        dvc_repo_url: str = 'https://github.com/AbdSipra/mlops-kubeflow-assignmen',
        dvc_data_path: str = 'data/raw_data.csv',
    ):
        data_extraction_task = data_extraction_component(
            dvc_repo_url=dvc_repo_url,
            dvc_data_path=dvc_data_path,
            output_csv_path='/tmp/raw_data.csv',
        ).set_display_name('Data Extraction')
        
        preprocessing_task = data_preprocessing_component(
            raw_csv_path=data_extraction_task.output,
            train_csv_path='/tmp/train.csv',
            test_csv_path='/tmp/test.csv',
        ).set_display_name('Data Preprocessing')
        
        training_task = model_training_component(
            train_csv_path=preprocessing_task.output,
            model_output_path='/tmp/model.joblib',
            n_estimators=100,
            random_state=42,
        ).set_display_name('Model Training')
        
        evaluation_task = model_evaluation_component(
            model_path=training_task.output,
            test_csv_path='/tmp/test.csv',
            metrics_output_path='/tmp/metrics.json',
        ).set_display_name('Model Evaluation')
    
    # Compile the pipeline
    Compiler().compile(boston_housing_pipeline, 'pipeline.yaml')
    print("✓ Pipeline compiled successfully to pipeline.yaml")
    
    # Verify the file exists
    if os.path.exists('pipeline.yaml'):
        file_size = os.path.getsize('pipeline.yaml')
        with open('pipeline.yaml', 'r') as f:
            lines = len(f.readlines())
        print(f"✓ pipeline.yaml verified: {lines} lines, {file_size} bytes")
    else:
        print("✗ ERROR: pipeline.yaml was not generated!")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
