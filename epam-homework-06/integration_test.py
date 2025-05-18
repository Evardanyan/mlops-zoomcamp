from datetime import datetime
from subprocess import run

from batch import  get_input_path, get_output_path, storage_client_kwargs

import pandas as pd

def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)


data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]
columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']

df = pd.DataFrame(data, columns=columns)

df_path = get_input_path(2021, 1)

df.to_parquet(
    df_path,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=storage_client_kwargs()
)

run(["python", "batch.py", "2021", "01"], check=True)

expected_output_path = get_output_path(2021, 1)

actual_df = pd.read_parquet(
    expected_output_path,
    storage_options=storage_client_kwargs())
print(actual_df.predicted_duration.sum())
assert round(actual_df.predicted_duration.sum()) == 36