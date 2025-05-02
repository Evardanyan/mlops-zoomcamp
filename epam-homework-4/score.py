#!/usr/bin/env python


import argparse
import pickle
import pandas as pd
import numpy as np
import os


parser = argparse.ArgumentParser()
parser.add_argument('--year', type=int, required=True, help='Year of the trip data')
parser.add_argument('--month', type=int, required=True, help='Month of the trip data')
args = parser.parse_args()

year = args.year
month = args.month

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet'
df = read_data(input_file)

df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

print(f"Mean predicted duration: {np.mean(y_pred):.2f}")

df_result = pd.DataFrame({
    'ride_id': df['ride_id'],
    'predicted_duration': y_pred
})

output_file = f'predictions_{year}_{month:02d}.parquet'
df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
print(f"Saved to {output_file}, size: {file_size_mb:.2f} MB")
