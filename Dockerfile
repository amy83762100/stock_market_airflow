FROM apache/airflow:2.6.2

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir duckdb kaggle lightgbm scikit-learn
