FROM apache/airflow:2.6.2

USER airflow

RUN pip install duckdb
RUN pip install kaggle
RUN pip install scikit-learn
