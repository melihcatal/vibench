import os
from ibm_watsonx_ai import APIClient

client = APIClient(
    apikey=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
)


def select_model(model_name):
    model = client.get_model(model_name)
    return model
