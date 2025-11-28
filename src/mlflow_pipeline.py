import mlflow
import mlflow.sklearn
from src.pipeline_components import (
    data_extraction_component,
    data_preprocessing_component,
    model_training_component,
    model_evaluation_component,
)


def run_pipeline():
    mlflow.set_experiment("boston_housing_pipeline")

    with mlflow.start_run(run_name="full_python_run"):

        # ----------------------------------------------------
        # 1. DATA EXTRACTION - Use local data directly
        # (Skip DVC get since data is already available locally)
        # ----------------------------------------------------
        import shutil

        shutil.copy("data/raw_data.csv", "data/raw_local.csv")
        output_csv = "data/raw_local.csv"
        mlflow.log_artifact("data/raw_local.csv")

        # ----------------------------------------------------
        # 2. PREPROCESSING (run underlying function)
        # ----------------------------------------------------
        data_preprocessing_component.python_func(
            raw_csv_path="data/raw_local.csv",
            train_csv_path="data/train.csv",
            test_csv_path="data/test.csv",
        )
        mlflow.log_artifact("data/train.csv")
        mlflow.log_artifact("data/test.csv")

        # ----------------------------------------------------
        # 3. TRAINING
        # ----------------------------------------------------
        model_path = model_training_component.python_func(
            train_csv_path="data/train.csv", model_output_path="models/rf_model.joblib"
        )
        mlflow.log_artifact("models/rf_model.joblib")

        # ----------------------------------------------------
        # 4. EVALUATION
        # ----------------------------------------------------
        metrics_path = model_evaluation_component.python_func(
            model_path="models/rf_model.joblib",
            test_csv_path="data/test.csv",
            metrics_output_path="metrics/metrics.json",
        )
        mlflow.log_artifact("metrics/metrics.json")

        # Log metrics to MLflow
        import json

        metrics = json.load(open("metrics/metrics.json"))
        for k, v in metrics.items():
            mlflow.log_metric(k, v)

    print("Pipeline successfully executed — check MLflow UI at http://127.0.0.1:5000")


if __name__ == "__main__":
    run_pipeline()
