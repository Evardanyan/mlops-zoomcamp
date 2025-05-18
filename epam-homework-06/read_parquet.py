# import pyarrow.parquet as pq

# table = pq.read_table('output/yellow_tripdata_2023-03.parquet')
# df = table.to_pandas()
# print("Shape:", df.shape)
# print(df.head())


import pandas as pd
import requests
from pathlib import Path

# --- Config ---
URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet"
LOCAL_PATH = Path("input/yellow_tripdata_2023-03.parquet")


def download_file(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(dest, "wb") as f:
        f.write(response.content)
    print(f"Downloaded and saved to {dest}")


def inspect_parquet_columns(path: Path):
    print(f"\nReading Parquet file: {path}")
    df = pd.read_parquet(path)
    print("\n✅ Columns in file:")
    for col in df.columns:
        print(f" - {col}")


if __name__ == "__main__":
    if not LOCAL_PATH.exists():
        download_file(URL, LOCAL_PATH)
    else:
        print(f"File already exists at {LOCAL_PATH}")

    inspect_parquet_columns(LOCAL_PATH)
