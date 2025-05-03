if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import numpy as np

@transformer
def transform(model_artifacts, _, df, **kwargs):
    """
    model_artifacts: [dv, model] from load_model block
    df: preprocessed DataFrame from preprocess block
    """
    dv, model = model_artifacts

    categorical = ['PULocationID', 'DOLocationID']
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    year = kwargs.get('year', 2023)
    month = kwargs.get('month', 5)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype(str)

    df['predicted_duration'] = y_pred

    print(f'Mean predicted duration: {np.mean(y_pred):.2f}')
    return df