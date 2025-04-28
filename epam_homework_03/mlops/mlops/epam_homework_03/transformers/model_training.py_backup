if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

@transformer
def transform(data, *args, **kwargs):
    """
    Train a Linear Regression model on taxi trip data.
    Returns the fitted DictVectorizer and the trained model.
    """

    
    # Define categorical features
    categorical = ['PULocationID', 'DOLocationID']

    # Convert to list of dicts
    train_dicts = data[categorical].to_dict(orient='records')

    # Initialize and fit DictVectorizer
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)

    # Target variable
    y_train = data['duration']

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Print the intercept
    print(f"Intercept: {model.intercept_}")

    return dv, model
