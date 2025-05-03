if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    df[['ride_id', 'predicted_duration']].to_parquet('/home/src/predictions.parquet', index=False)

