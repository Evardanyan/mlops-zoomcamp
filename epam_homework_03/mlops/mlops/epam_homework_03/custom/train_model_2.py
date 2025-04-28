if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression



@transformer
def transform_custom(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here

    print('DEBUG:', type(data))
    
    categorical = ['PULocationID', 'DOLocationID']
    train_dicts = data[categorical].to_dict(orient='records')

    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)

    y_train = data['duration']

    model = LinearRegression()
    model.fit(X_train, y_train)

    print(f"Intercept: {model.intercept_}")

    return dv, model

