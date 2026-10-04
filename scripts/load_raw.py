"""Load Upworthy archive CSVs into BigQuery raw dataset (all columns as STRING)."""

import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT_ID = os.environ["GCP_PROJECT_ID"]
LOCATION = "asia-northeast1"
DATASET = "raw"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

FILES = {
    "packages_exploratory": "upworthy-archive-exploratory-packages-03.12.2020.csv",
    "packages_confirmatory": "upworthy-archive-confirmatory-packages-03.12.2020.csv",
}

COLUMNS = [
    "row_index", "created_at", "updated_at", "clickability_test_id", "excerpt",
    "headline", "lede", "slug", "eyecatcher_id", "impressions", "clicks",
    "significance", "first_place", "winner", "share_text", "square", "test_week",
]


def main() -> None:
    client = bigquery.Client(project=PROJECT_ID, location=LOCATION)

    dataset = bigquery.Dataset(f"{PROJECT_ID}.{DATASET}")
    dataset.location = LOCATION
    client.create_dataset(dataset, exists_ok=True)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=[bigquery.SchemaField(c, "STRING") for c in COLUMNS],
        allow_quoted_newlines=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    for table_name, file_name in FILES.items():
        table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"
        with open(DATA_DIR / file_name, "rb") as f:
            job = client.load_table_from_file(f, table_id, job_config=job_config)
        job.result()
        table = client.get_table(table_id)
        print(f"Loaded {table.num_rows} rows into {table_id}")


if __name__ == "__main__":
    main()