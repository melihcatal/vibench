import os
from ibm_watsonx_ai import APIClient

client = APIClient()


def stream_generation(model_id, input_data):
    response = client.generate(model_id=model_id, input=input_data, stream=True)
    for chunk in response:
        yield chunk
