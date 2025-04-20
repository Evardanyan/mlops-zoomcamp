# import os
# import pickle
# import click

# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error


# def load_pickle(filename: str):
#     with open(filename, "rb") as f_in:
#         return pickle.load(f_in)


# @click.command()
# @click.option(
#     "--data_path",
#     default="./output",
#     help="Location where the processed NYC taxi trip data was saved"
# )
# def run_train(data_path: str):

#     X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
#     X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

#     rf = RandomForestRegressor(max_depth=10, random_state=0)
#     rf.fit(X_train, y_train)
#     y_pred = rf.predict(X_val)

#     rmse = mean_squared_error(y_val, y_pred, squared=False)


# if __name__ == '__main__':
#     run_train()

# modified  to use mlflow

import os
import pickle
import click

import mlflow
import mlflow.sklearn

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):

    mlflow.sklearn.autolog()

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    mlflow.set_experiment("green-taxi-experiment")
    mlflow.sklearn.autolog()

    with mlflow.start_run():
        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        rmse = mean_squared_error(y_val, y_pred, squared=False)
        print(f"RMSE: {rmse}")
        print(f"🔍 min_samples_split: {rf.get_params()['min_samples_split']}")


if __name__ == '__main__':
    run_train()
