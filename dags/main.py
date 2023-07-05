from datetime import datetime
from dotenv import load_dotenv

from airflow import DAG
from airflow.operators.python import PythonOperator

from download_data import download_data


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

    download_data
