if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data(df, *args, **kwargs):
    """
    df: Output from predict_3 block
    """
    print(f'Saving predictions, df shape: {df.shape}')
    
    return df[['ride_id', 'predicted_duration']]

# homework_04_fully done!
