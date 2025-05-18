#!/usr/bin/env python
# coding: utf-8
import pickle
import os
from pathlib import Path
import logging

import pandas as pd

import sys

import requests

CATEGORICAL = ["PULocationID", "DOLocationID"]

def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration-prediction-alexey/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)


def storage_client_kwargs() -> dict:
    """
    Returns a dictionary with client_kwargs for S3 storage options.
    This is used to configure the S3 client when reading/writing data.
    """
    s3_endpoint_url = os.getenv('S3_ENDPOINT_URL')
    if s3_endpoint_url is not None:
        return {
            'client_kwargs': {
                'endpoint_url': s3_endpoint_url
            }
        }
    return None

def download_data(url: str, local_path: str):
    """
    Download a remote file via HTTP and store it locally.
    """
    if url.startswith("http"):
        logging.info(f"Downloading file from {url} to {local_path}")
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(response.content)
        logging.info(f"Downloaded and saved to {local_path}")
        return local_path
    return url

def prepare_data(df, categorical):
    df['duration'] = df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

# def read_data(path: str, categorical: list[str]) -> pd.DataFrame:
#     df = pd.read_parquet(path, storage_options=storage_client_kwargs())

#     df = prepare_data(df, categorical)

#     return df


def read_data(path: str, categorical: list[str]) -> pd.DataFrame:
    try:
        df = pd.read_parquet(path, storage_options=storage_client_kwargs())
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Failed to read Parquet file: {path}\n{e}")

    return prepare_data(df, categorical)

def save_data(df, output_path):
    df.to_parquet(
        output_path,
        engine='pyarrow',
        index=False,
        compression=None,
        storage_options=storage_client_kwargs()
    )


def main(year: int, month: int):
    # categorical = ["PULocationID", "DOLocationID"]
    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    input_file = get_input_path(year, month)
    output_path = get_output_path(year, month)

    df = read_data(input_file, CATEGORICAL)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    dicts = df[CATEGORICAL].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    print('predicted mean duration:', y_pred.mean())
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    save_data(df_result, output_path)


if __name__ == "__main__":
    y, m = map(int, sys.argv[1:3])
    main(y, m)
    # year = int(sys.argv[1])
    # month = int(sys.argv[2])
    # main(year, month)
