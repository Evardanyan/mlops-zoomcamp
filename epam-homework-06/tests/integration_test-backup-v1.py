import pandas as pd
import os

# Define dummy test input data (same as in unit test)
data = {
    "PULocationID": [1, 2, 3],
    "DOLocationID": [11, 22, 33],
    "tpep_pickup_datetime": pd.to_datetime(["2023-01-01 00:00:00"] * 3),
    "tpep_dropoff_datetime": pd.to_datetime(["2023-01-01 00:10:00", "2023-01-01 00:20:00", "2023-01-01 00:30:00"]),
}

# Create DataFrame
df_input = pd.DataFrame(data)

# Define input path in S3 (pretend it's for January 2023)
input_file = "s3://nyc-duration/in/2023-01.parquet"

# S3-compatible storage options for LocalStack
options = {
    "client_kwargs": {
        "endpoint_url": os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
    }
}

# Save to Parquet on S3 (as required by the question)
df_input.to_parquet(
    input_file,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)

print(f"Test data written to {input_file}")
