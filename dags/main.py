from datetime import datetime
from dotenv import load_dotenv

from airflow import DAG
from airflow.operators.python import PythonOperator

from download_data import download_data
from data_processing import raw_data_processing, feature_engineering
from ml_training import ml_training


DAG_ID = "stock_etf_data_pipeline"

default_args = {
    "owner": "stock_market",
    "depends_on_past": False,
    "retries": 0,
}

load_dotenv()

with DAG(
    DAG_ID,
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2023, 7, 5),
    catchup=False,
    tags=["stocks", "etfs", "data-pipeline"],
) as dag:
    download_data = PythonOperator(
        task_id="download_data",
        python_callable=download_data,
    )

    etfs_raw_data_processing = PythonOperator(
        task_id="etfs_raw_data_processing",
        python_callable=raw_data_processing,
        op_kwargs={"stockType": "etfs"},
    )

    stocks_raw_data_processing = PythonOperator(
        task_id="stocks_raw_data_processing",
        python_callable=raw_data_processing,
        op_kwargs={"stockType": "stocks"},
    )

    feature_engineering = PythonOperator(
        task_id="feature_engineering",
        python_callable=feature_engineering,
    )

    ml_training = PythonOperator(
        task_id="ml_training",
        python_callable=ml_training,
    )

    (
        download_data
        >> [etfs_raw_data_processing, stocks_raw_data_processing]
        >> feature_engineering
        >> ml_training
    )
