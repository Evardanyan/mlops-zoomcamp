if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(data, *args, **kwargs):
    """
    Prepare the Yellow Taxi trip dataset:
    - Parse datetime fields
    - Calculate duration in minutes
    - Filter trips between 1 and 60 minutes
    - Convert location IDs to strings
    """

    # Ensure datetime parsing
    data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])
    data['tpep_dropoff_datetime'] = pd.to_datetime(data['tpep_dropoff_datetime'])

    # Calculate trip duration in minutes
    data['duration'] = (data['tpep_dropoff_datetime'] - data['tpep_pickup_datetime']).dt.total_seconds() / 60

    # Keep only trips with duration between 1 and 60 minutes
    data = data[(data['duration'] >= 1) & (data['duration'] <= 60)]

    # Convert categorical features to strings
    categorical = ['PULocationID', 'DOLocationID']
    data[categorical] = data[categorical].astype(str)

    return data

# @test
# def test_output(output, *args) -> None:
#     """
#     Test to ensure that the output of the block is valid.
#     """
#     assert output is not None, 'The output is undefined'
#     assert len(output) == 3103766, f"Expected 3,103,766 rows, but got {len(output)}"
