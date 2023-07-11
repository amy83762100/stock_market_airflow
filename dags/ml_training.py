import os
import psutil
import time


def ml_training(ti):
    """
    Perform machine learning training on the preprocessed data.

    Args:
        ti (TaskInstance): The Airflow task instance.
    """

    import pandas as pd
    import joblib
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    import lightgbm as lgb

    filename = ti.xcom_pull(task_ids="feature_engineering")
    # Load the data
    data = pd.read_parquet(filename)

    # Get the process ID and create a process object
    pid = os.getpid()
    process = psutil.Process(pid)
    start = time.time()

    # Remove rows with NaN values
    data.dropna(inplace=True)

    # Select features and target
    features = ["vol_moving_avg", "adj_close_rolling_med"]
    target = "Volume"

    X = data[features]
    y = data[target]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    d_train = lgb.Dataset(X_train, label=y_train)

    # Setting parameters
    param = {
        "num_leaves": 100,
        "max_depth": 10,
        "boosting": "dart",
        "force_row_wise": True,
    }  # learning rate: 0.1
    num_round = 100

    # Train the model
    model = lgb.train(param, d_train, num_round)

    # Get the process time
    end = time.time()
    print("Time:", end - start, "seconds")

    # Get the memory usage of the process
    memory_info = process.memory_info()

    # Convert the memory usage to megabytes
    memory_usage_mb = memory_info.rss / (1024 * 1024)
    print("Memory usage:", memory_usage_mb, "MB")

    # Make predictions on test data
    y_pred = model.predict(X_test)

    # Calculate the Mean Absolute Error and Mean Squared Error
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    # Save the model
    ml_dir = os.path.abspath(
        os.path.join(os.path.realpath(__file__), "../../data/ml_training")
    )
    os.makedirs(ml_dir, exist_ok=True)
    print(f"Saving model to {ml_dir}/model.joblib")
    model_filename = f"{ml_dir}/model.joblib"
    joblib.dump(model, model_filename)

    # Persist training metrics as log files
    with open(f"{ml_dir}/mae.log", "w") as f:
        f.write(str(mae))
    with open(f"{ml_dir}/mse.log", "w") as f:
        f.write(str(mse))
