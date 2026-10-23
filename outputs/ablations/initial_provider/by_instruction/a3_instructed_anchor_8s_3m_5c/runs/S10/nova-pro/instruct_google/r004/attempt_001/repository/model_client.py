import os
from google.cloud import aiplatform

def get_client():
    client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    return aiplatform.gapic.PredictionServiceClient(client_options=client_options)

def get_endpoint(endpoint_name):
    return os.getenv(endpoint_name)