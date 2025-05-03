import numpy as np

@custom
def transform_custom(df, model_output, **kwargs):
    dv, model = model_output
    categorical = ['PULocationID', 'DOLocationID']

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    df['ride_id'] = f"{kwargs['year']:04d}/{kwargs['month']:02d}_" + df.index.astype('str')
    print(f"Mean predicted duration: {np.mean(y_pred):.2f}")

    return df[['ride_id']], y_pred


