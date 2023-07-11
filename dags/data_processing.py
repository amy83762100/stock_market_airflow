import os
import duckdb


def raw_data_processing(stockType: str, ti):
    """
    Process raw data for a given stock type and convert it to Parquet format.

    Args:
        stockType (str): The type of stock (e.g., ETF, stock).
        ti (TaskInstance): The Airflow task instance.

    Returns:
        str: The directory path where the processed data is stored.
    """
    # Setup a data structure to retain all data from ETFs and stocks
    # Convert the resulting dataset into Parquet format
    data_dir = ti.xcom_pull(task_ids="download_data")
    processed_dir = os.path.join(data_dir, "processed")
    stockType_dir = os.path.join(data_dir, stockType)
    os.makedirs(processed_dir, exist_ok=True)
    query = f"""
    COPY (
        WITH stock AS (
            SELECT 
                *,
                regexp_extract(filename, '\/(\w*).csv', 1) AS Symbol
            FROM read_csv(
                '{stockType_dir}/*.csv',
                header=True,
                columns={{
                    'Date': 'VARCHAR',
                    'Open': 'DOUBLE',
                    'High': 'DOUBLE',
                    'Low': 'DOUBLE',
                    'Close': 'DOUBLE',
                    'Adj Close': 'DOUBLE',
                    'Volume': 'BIGINT'
                }},
                filename=True
            )
        )
        SELECT 
            sy.Symbol,
            sy."Security Name",
            s.Date,
            s.Open,
            s.High,
            s.Low,
            s.Close,
            s."Adj Close",
            s.Volume
        FROM read_csv_auto('{data_dir}/symbols_valid_meta.csv', header=True) sy
        JOIN stock s
            ON s.Symbol = sy.Symbol
    )TO '{processed_dir}/{stockType}.parquet' (FORMAT 'parquet', CODEC 'ZSTD')
    """
    conn = duckdb.connect()
    conn.sql(query)

    r = conn.sql(f"DESCRIBE SELECT * FROM '{processed_dir}/{stockType}.parquet'")
    print(f"{processed_dir}/{stockType}.parquet schema:", r)

    return processed_dir


def feature_engineering(ti):
    """
    Perform feature engineering on processed data by calculating moving averages and rolling medians.

    Args:
        ti (TaskInstance): The Airflow task instance.

    Returns:
        str: The file path of the processed data with added features.
    """

    # Calculate the moving average of the trading volume (Volume) of 30 days per each stock and ETF, and retain it in a newly added column vol_moving_avg.
    # Calculate the rolling median and retain it in a newly added column adj_close_rolling_med.
    processed_dir = ti.xcom_pull(task_ids="stocks_raw_data_processing")
    feature_engineering_dir = os.path.join(processed_dir, "feature_engineering")

    os.makedirs(feature_engineering_dir, exist_ok=True)
    filename = f"{feature_engineering_dir}/stocks_etfs.parquet"
    query = f"""
    COPY (
        SELECT 
            *,
            AVG(Volume) OVER (
                PARTITION BY Symbol
                ORDER BY strptime(Date,'%Y-%m-%d')
                RANGE BETWEEN INTERVAL '29 days' PRECEDING AND CURRENT ROW
            ) AS vol_moving_avg,
            QUANTILE_CONT("Adj Close", 0.5) OVER (
                PARTITION BY Symbol
                ORDER BY strptime(Date,'%Y-%m-%d')
                RANGE BETWEEN INTERVAL '29 days' PRECEDING AND CURRENT ROW
            ) AS adj_close_rolling_med
        FROM read_parquet('{processed_dir}/*.parquet')
        WHERE Volume IS NOT NULL
            AND "Adj Close" IS NOT NULL
    )TO '{filename}' (FORMAT 'parquet', CODEC 'ZSTD')
    """
    conn = duckdb.connect()
    conn.sql(query)

    r = conn.sql(f"DESCRIBE SELECT * FROM '{filename}'")
    print(f"{filename} schema:", r)
    return filename
