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
    """
    Complete ML pipeline for Boston Housing dataset.

    Steps:
    1. Extract data from DVC-tracked repository
    2. Preprocess: clean, scale, and split data
    3. Train: Random Forest model
    4. Evaluate: calculate metrics (MSE, R2)
    """

    # Step 1: Data Extraction
    data_extraction_task = data_extraction_component(
        dvc_repo_url=dvc_repo_url,
        dvc_data_path=dvc_data_path,
        output_csv_path="/tmp/raw_data.csv",
    ).set_display_name("Data Extraction")

    # Step 2: Data Preprocessing
    preprocessing_task = data_preprocessing_component(
        raw_csv_path=data_extraction_task.output,
        train_csv_path="/tmp/train.csv",
        test_csv_path="/tmp/test.csv",
        test_size=0.2,
        random_state=42,
    ).set_display_name("Data Preprocessing")

    # Step 3: Model Training
    training_task = model_training_component(
        train_csv_path=preprocessing_task.output,
        model_output_path="/tmp/model.joblib",
        n_estimators=100,
        random_state=42,
    ).set_display_name("Model Training")

    # Step 4: Model Evaluation
    evaluation_task = model_evaluation_component(
        model_path=training_task.output,
        test_csv_path="/tmp/test.csv",
        metrics_output_path="/tmp/metrics.json",
    ).set_display_name("Model Evaluation")


if __name__ == "__main__":
    # Compile the pipeline
    compiler.Compiler().compile(
        pipeline_func=boston_housing_pipeline,
        package_path="pipeline.yaml",
    )
    print("✓ Pipeline compiled successfully to pipeline.yaml")
