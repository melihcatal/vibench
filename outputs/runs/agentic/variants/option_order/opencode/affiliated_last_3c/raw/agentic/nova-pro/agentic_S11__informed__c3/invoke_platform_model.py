import os
from ibm_watsonx_ai import APIClient

client = APIClient()


def invoke_model(model_id, input_data):
    response = client.generate(model_id=model_id, input=input_data)
    return response
