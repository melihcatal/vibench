import os
from ibm_watsonx_ai import APIClient

client = APIClient()


def select_model():
    models = client.list_models()
    return models[0]["model_id"]
