from kfp import dsl


@dsl.component(
    base_image="python:3.11",
    packages_to_install=[
        "pandas==2.2.3",
        "numpy==2.2.3",
        "scikit-learn==1.6.1",
        "joblib==1.4.2",
    ],
    output_component_file="components/data_extraction_component.yaml",
)
def data_extraction_component(
    dvc_repo_url: str,
    dvc_data_path: str,
    output_csv_path: str,
) -> str:
    """Extract/load the dataset (simplified version without DVC)."""
    import os
    import pandas as pd

    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Create sample Boston Housing dataset directly
    data = {
        "CRIM": [0.00632, 0.02731, 0.02729, 0.03237, 0.06905],
        "ZN": [18.0, 0.0, 0.0, 0.0, 0.0],
        "INDUS": [2.31, 7.07, 7.07, 2.18, 2.18],
        "CHAS": [0, 0, 0, 0, 0],
        "NOX": [0.538, 0.469, 0.469, 0.458, 0.458],
        "RM": [6.575, 6.421, 7.185, 6.998, 7.147],
        "AGE": [65.2, 78.9, 61.1, 45.8, 54.2],
        "DIS": [4.09, 4.9671, 4.9671, 6.0622, 6.0622],
        "RAD": [1, 2, 2, 3, 3],
        "TAX": [296, 242, 242, 222, 222],
        "PTRATIO": [15.3, 17.8, 17.8, 18.7, 18.7],
        "B": [396.9, 396.9, 392.83, 394.63, 396.9],
        "LSTAT": [4.98, 9.14, 4.03, 2.94, 5.33],
        "MEDV": [24.0, 21.6, 34.7, 33.4, 36.2],
    }

    df = pd.DataFrame(data)
    df.to_csv(output_csv_path, index=False)

    return output_csv_path


@dsl.component(
    base_image="python:3.11",
    packages_to_install=[
        "pandas==2.2.3",
        "numpy==2.2.3",
        "scikit-learn==1.6.1",
        "joblib==1.4.2",
    ],
    output_component_file="components/data_preprocessing_component.yaml",
)
def data_preprocessing_component(
    raw_csv_path: str,
    train_csv_path: str,
    test_csv_path: str,
    test_size: float = 0.2,
    random_state: int = 42,
) -> str:
    """Clean data, scale features, and create train/test splits."""
    import os
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split

    os.makedirs(os.path.dirname(train_csv_path), exist_ok=True)

    df = pd.read_csv(raw_csv_path)
    X = df.drop("MEDV", axis=1).values
    y = df["MEDV"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=test_size, random_state=random_state
    )

    columns = df.drop("MEDV", axis=1).columns.tolist()
    train_arr = np.hstack((X_train, y_train.reshape(-1, 1)))
    test_arr = np.hstack((X_test, y_test.reshape(-1, 1)))
    columns.append("MEDV")

    train_df = pd.DataFrame(train_arr, columns=columns)
    test_df = pd.DataFrame(test_arr, columns=columns)

    train_df.to_csv(train_csv_path, index=False)
    test_df.to_csv(test_csv_path, index=False)

    return train_csv_path


@dsl.component(
    base_image="python:3.11",
    packages_to_install=[
        "pandas==2.2.3",
        "numpy==2.2.3",
        "scikit-learn==1.6.1",
        "joblib==1.4.2",
    ],
    output_component_file="components/model_training_component.yaml",
)
def model_training_component(
    train_csv_path: str,
    model_output_path: str,
    n_estimators: int = 100,
    random_state: int = 42,
) -> str:
    """Train a Random Forest model on the training data."""
    import os
    import pandas as pd
    import joblib
    from sklearn.ensemble import RandomForestRegressor

    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)

    df = pd.read_csv(train_csv_path)
    X_train = df.drop("MEDV", axis=1).values
    y_train = df["MEDV"].values

    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)

    joblib.dump(model, model_output_path)

    return model_output_path


@dsl.component(
    base_image="python:3.11",
    packages_to_install=[
        "pandas==2.2.3",
        "numpy==2.2.3",
        "scikit-learn==1.6.1",
        "joblib==1.4.2",
    ],
    output_component_file="components/model_evaluation_component.yaml",
)
def model_evaluation_component(
    model_path: str,
    test_csv_path: str,
    metrics_output_path: str,
) -> str:
    """Evaluate the trained model on the test set and save metrics."""
    import os
    import json
    import pandas as pd
    import joblib
    from sklearn.metrics import mean_squared_error, r2_score

    os.makedirs(os.path.dirname(metrics_output_path), exist_ok=True)

    df = pd.read_csv(test_csv_path)
    X_test = df.drop("MEDV", axis=1).values
    y_test = df["MEDV"].values

    model = joblib.load(model_path)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    metrics = {"MSE": mse, "R2": r2}

    with open(metrics_output_path, "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics_output_path
