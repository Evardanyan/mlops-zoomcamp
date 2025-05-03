import pandas as pd

@data_loader
def load_data(*args, **kwargs):
    year = kwargs.get('year', 2023)
    month = kwargs.get('month', 5)
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet'

    df = pd.read_parquet(url)
    return df
