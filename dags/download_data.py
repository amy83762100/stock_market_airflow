import os

from airflow.exceptions import AirflowFailException


def download_data():
    """
    Download ETF and stock datasets from Kaggle.

    Returns:
        str: The directory path where the data is downloaded.

    Raises:
        AirflowFailException: If the Kaggle username or key is not set.
    """

    import kaggle

    # Download the ETF and stock datasets from the primary dataset available at https://www.kaggle.com/datasets/jacksoncrow/stock-market-dataset.
    root = os.path.abspath(os.path.join(os.path.realpath(__file__), "../../"))
    data_dir = os.path.join(root, "data")

    kaggle_username = os.getenv("KAGGLE_USERNAME")
    kaggle_key = os.getenv("KAGGLE_KEY")

    if not kaggle_username or not kaggle_key:
        raise AirflowFailException("Kaggle username or key is not set")
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(
        "jacksoncrow/stock-market-dataset", path=data_dir, unzip=True
    )

    return data_dir
