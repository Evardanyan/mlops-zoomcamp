# if 'data_exporter' not in globals():
#     from mage_ai.data_preparation.decorators import data_exporter

# import mlflow
# import mlflow.sklearn
# import os
# import pickle

# @data_exporter
# def export_data(dv_model_tuple, *args, **kwargs):
#     """
#     Export trained model and DictVectorizer to MLflow
#     """

#     # Unpack tuple
#     dv, model = dv_model_tuple

#     # Set MLflow tracking URI (talk to MLflow container inside Docker network)
#     mlflow.set_tracking_uri("http://mlflow:5000")

#     # Start MLflow run
#     with mlflow.start_run():

#         # Log the trained LinearRegression model
#         mlflow.sklearn.log_model(
#             sk_model=model,
#             artifact_path="model",
#             registered_model_name="yellow_taxi_duration_model"
#         )

#         # Save DictVectorizer manually
#         dv_path = '/tmp/dv.pkl'
#         with open(dv_path, 'wb') as f_out:
#             pickle.dump(dv, f_out)

#         # Log the DictVectorizer as artifact
#         mlflow.log_artifact(dv_path, artifact_path="dict_vectorizer")


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import mlflow
import mlflow.sklearn
import os
import pickle

print("DEBUG: mage sees this block loaded.")

@data_exporter
def export_data(dv_model_tuple, *args, **kwargs):
    """
    Export trained model and DictVectorizer to MLflow
    """
    print("DEBUG: Starting export_data...")

    # Unpack tuple
    dv, model = dv_model_tuple
    print("DEBUG: Tuple unpacked. Got DictVectorizer and model.")

    # Set MLflow tracking URI
    mlflow.set_tracking_uri("http://mlflow:5000")
    print("DEBUG: MLflow tracking URI set.")

    # Start MLflow run
    print("DEBUG: About to start mlflow run...")
    with mlflow.start_run():
        print("DEBUG: MLflow run started.")

        # Log the trained LinearRegression model
        print("DEBUG: About to log model...")
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="yellow_taxi_duration_model"
        )
        print("DEBUG: Model logged.")

        # Save DictVectorizer manually
        dv_path = '/tmp/dv.pkl'
        print("DEBUG: About to save DictVectorizer...")
        with open(dv_path, 'wb') as f_out:
            pickle.dump(dv, f_out)
        print(f"DEBUG: DictVectorizer saved at {dv_path}.")

        # Log the DictVectorizer as artifact
        print("DEBUG: About to log DictVectorizer artifact...")
        mlflow.log_artifact(dv_path, artifact_path="dict_vectorizer")
        print("DEBUG: DictVectorizer artifact logged.")

    print("DEBUG: export_data finished successfully!")


