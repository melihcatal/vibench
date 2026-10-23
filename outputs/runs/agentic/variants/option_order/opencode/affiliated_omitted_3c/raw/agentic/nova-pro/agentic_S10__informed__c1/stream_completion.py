import os
from ibm_watsonx_ai import ModelClient

client = ModelClient(os.getenv("WATSONX_API_KEY"), os.getenv("WATSONX_PROJECT_ID"))


def stream_completion(prompt):
    response = client.stream_completion(prompt)
    return response
