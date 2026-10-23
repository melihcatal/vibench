import os
from ibm_watsonx_ai import ModelClient

client = ModelClient(os.getenv("WATSONX_API_KEY"), os.getenv("WATSONX_PROJECT_ID"))


def extract_json(text):
    response = client.extract_json(text)
    return response
