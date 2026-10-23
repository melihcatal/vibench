import os
from google.cloud import aiplatform


def get_client():
    client_options = {"api_endpoint": os.getenv("AI_PLATFORM_ENDPOINT")}
    return aiplatform.gapic.PredictionServiceClient(client_options=client_options)


def get_model_name():
    return os.getenv("MODEL_NAME")
