import os
import pandas as pd

endpoint_url = os.getenv("S3_ENDPOINT_URL")
path = "s3://nyc-duration/in/2023-03.parquet"
storage_options = {"client_kwargs": {"endpoint_url": endpoint_url}}

df = pd.read_parquet(path, storage_options=storage_options)
print(df.columns)
