# Stock Market Data Processing App

This is a data processing application for ingesting and processing raw stock market datasets. It leverages Airflow to create a data pipeline that performs various tasks on the data.

## Airflow DAG Diagram

![Screenshot 2023-07-06 at 2 10 15 AM](https://github.com/amy83762100/stock_market_airflow/assets/76548841/409f9d01-3282-489c-8f2c-c5397c51764a)

The above diagram illustrates the workflow of the data pipeline implemented using Airflow. It shows the tasks and their dependencies.

## Prerequisites

Before running this application, please make sure you have the following:

- Docker installed on your machine
- A Kaggle account

## Getting Started

To run this application, follow these steps:

1. Obtain a Kaggle API token:
   - Go to [kaggle.com](https://www.kaggle.com)
   - Sign in or create a Kaggle account
   - Go to your account settings page
   - Scroll down to the "API" section and click on "Create New API Token"
   - Download `kaggle.json` file
   - Open the `docker-compose.yml` file in a text editor
   - Replace `<KAGGLE_USERNAME>` with your Kaggle username
   - Replace `<KAGGLE_KEY>` with your Kaggle API key

2. Build and start the Docker containers:
   - Open a terminal and navigate to the project's root directory
   - Run the following command to start the Docker containers:
     ```
     docker-compose up
     ```

3. Wait for the containers to start and the Airflow web interface to become available. You can access the Airflow web UI at [http://localhost:8080](http://localhost:8080).
   - Username: airflow
   - Password: airflow

4. In the Airflow web UI, locate and trigger the DAG to begin processing the datasets.

5. Monitor the progress of the DAG execution in the Airflow web UI. Once the processing is complete, you can find the resulting dataset in the `data/processed` folder and the trained predictive model in `data/ml_training` folder.

## Using the API Server

### Live Deployment

For a live deployment of the API server, you can access the following URL:

[https://stock-market-api-v1-0c7118cdd11c.herokuapp.com/predict?vol_moving_avg=12345&adj_close_rolling_med=25](https://stock-market-api-v1-0c7118cdd11c.herokuapp.com/predict?vol_moving_avg=12345&adj_close_rolling_med=25)

Replace `vol_moving_avg` and `adj_close_rolling_med` with the desired values for the moving average of trading volume and rolling median of adjusted close.

### Local Deployment

To make predictions using the trained predictive model locally, you can start the API server with the following steps:

1. Install the required dependencies by running the following command:
   ```
   pipenv install
   ```

2. Start the API server by running the following command:
   ```
   pipenv run python api.py
   ```


3. The API server will be running at `http://127.0.0.1:5000`.

4. To make predictions, access the `/predict` endpoint with the required input parameters. For example:
   ```
   http://127.0.0.1:5000/predict?vol_moving_avg=12345&adj_close_rolling_med=25
   ```

## Model Selection and Performance Comparison

I experimented with different models to assess their performance and select the most suitable one based on specific requirements. Here are the results of the conducted experiments:

###  Experiment 1: RandomForestRegressor (Baseline)

Previously, the RandomForestRegressor algorithm was used with the following parameters:
   ```
RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42, n_jobs=-1)
   ```
- Result:
    - Time: 744.51 seconds
    - Memory usage: 483.18 MB
    - MAE: 484,881.77
    - MSE: 44,442,244,640,816.66

###  Experiment 2: LightGBM (boosting='gbdt')

A transition was made from the RandomForestRegressor to LightGBM to improve predictive accuracy and processing speed. The first experiment with LightGBM used the 'gbdt' boosting type and the following parameters:
   ```
    param = {'num_leaves': 75, 'max_depth': 10} # boosting: 'gbdt', learning rate: 0.1
    num_round = 100
   ```
- Result:
    - Time: 57.46 seconds
    - Memory usage: 5807.49 MB
    - MAE: 479,776.44
    - MSE: 69,650,280,259,173.53

###  Experiment 3: LightGBM (boosting='dart')

Another experiment was conducted with LightGBM, this time using the 'dart' boosting type, which introduces dropouts during the tree-building process. The following parameters were used:
   ```
    param = {'num_leaves': 100, 'max_depth': 10, 'boosting': 'dart'} # learning rate: 0.1
    num_round = 100
   ```
- Result:
    - Time: 257.43 seconds
    - Memory usage: 4806.63 MB
    - MAE: 460,743.43
    - MSE: 71,709,656,974,918.84

###  Experiment 4: LightGBM (boosting='gbdt', 'force_row_wise': True)

To explore additional variations, a new experiment was conducted with LightGBM using the 'gbdt' boosting type and the 'force_row_wise' parameter set to True.
   ```
    param = {'num_leaves': 75, 'max_depth': 10, 'force_row_wise': True} # boosting: 'gbdt', learning rate: 0.1
    num_round = 100
   ```
- Result:
    - Time: 90.87 seconds
    - Memory usage: 1770.69 MB
    - MAE: 479,776.44
    - MSE: 69,650,280,259,173.53

###  Experiment 5: LightGBM (boosting='dart', 'force_row_wise': True)

To explore additional variations, a new experiment was conducted with LightGBM using the 'gbdt' boosting type and the 'force_row_wise' parameter set to True.
   ```
    param = {'num_leaves': 100, 'max_depth': 10, 'boosting': 'dart', 'force_col_wise': True} # learning rate: 0.1
    num_round = 100
   ```
- Result:
    - Time: 655.01 seconds
    - Memory usage: 611.24 MB
    - MAE: 460,743.43
    - MSE: 71,709,656,974,918.84

The full experiment log can be found in [docs/ml_model_experiment_results.txt](https://github.com/amy83762100/stock_market_airflow/blob/main/docs/ml_model_experiment_results.txt)

### Model Selection and Trade-offs

- The LightGBM model with 'dart' boosting demonstrated lower MAE compared to the 'gbdt' boosting variant.
- However, the 'gbdt' boosting variant showed faster execution time and lower memory usage compared to 'dart'.
- The 'force_row_wise' parameter, set to True in some experiments, optimized memory usage by reducing the internal memory footprint.

- If minimizing memory usage and execution time are the primary concerns, the 'gbdt' variation may be preferable. It provides a reasonable MAE while demonstrating faster performance and lower memory requirements.

- However, if optimizing prediction accuracy is the top priority and the available computational resources can accommodate the increased memory usage and longer execution time, the 'dart' variation may be the better choice. It achieves a lower MAE, indicating more accurate predictions.

### Conclusion
After conducting several [experiments](https://github.com/amy83762100/stock_market_airflow/blob/main/docs/ml_model_experiment_results.txt), LightGBM was chosen due to its promising performance. The following parameters were selected for LightGBM:
   ```
param = {'num_leaves': 100, 'max_depth': 10, 'boosting': 'dart', 'force_col_wise': True} # learning rate: 0.1
num_round = 100
model = lgb.train(param, d_train, num_round)

   ```
Transitioning from RandomForestRegressor to LightGBM have improved the predictive accuracy and overall speed of the model. Through experimentation, it was determined that using LightGBM with the 'dart' boosting type achieved a better MAE compared to the default 'gbdt' boosting type. The chosen LightGBM model demonstrated improved performance and showed potential for accurate predictions.

(Considering that the outliers in the data do not have a significant impact, prioritizing the Mean Absolute Error (MAE) aligns with the objective of achieving accurate predictions.)
