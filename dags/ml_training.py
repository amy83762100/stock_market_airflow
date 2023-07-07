import os


def ml_training(ti):
    """
    Perform machine learning training on the preprocessed data.

    Args:
        ti (TaskInstance): The Airflow task instance.
    """

    import pandas as pd
    import joblib
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    filename = ti.xcom_pull(task_ids="feature_engineering")
    # Load the data
    data = pd.read_parquet(filename)
    data["Date"] = pd.to_datetime(data["Date"])
    data.set_index("Date", inplace=True)

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

    # Create a RandomForestRegressor model
    model = RandomForestRegressor(
        n_estimators=50, max_depth=5, random_state=42, n_jobs=-1
    )

    # Train the model
    model.fit(X_train, y_train)

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
