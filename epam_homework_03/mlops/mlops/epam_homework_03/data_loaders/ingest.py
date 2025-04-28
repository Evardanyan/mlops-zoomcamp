if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@data_loader
def load_data(*args, **kwargs):
    """
    Loads Yellow Taxi trip data for March 2023.

    Returns:
        pd.DataFrame: DataFrame containing taxi trip records.
    """
    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'
    
    # Load the parquet file directly into a DataFrame
    df = pd.read_parquet(url)
    
    return df

@test
def test_output(output, *args) -> None:
    """
    Test to ensure that the output is not None and has expected number of rows.
    """
    assert output is not None, 'The output is undefined'
    assert len(output) == 3403766, f"Expected 3,403,766 rows, but got {len(output)}"