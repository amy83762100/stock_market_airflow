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
