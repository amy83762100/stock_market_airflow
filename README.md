# Stock Market Data Processing App

This is a data processing application for ingesting and processing raw stock market datasets. It leverages Airflow to create a data pipeline that performs various tasks on the data.

## Airflow DAG Diagram

![Screenshot 2023-07-06 at 2 10 15 AM](https://github.com/amy83762100/stock_market_airflow/assets/76548841/ffd9d60e-9b9e-46c0-8aa1-5f2b9290d6fe)

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