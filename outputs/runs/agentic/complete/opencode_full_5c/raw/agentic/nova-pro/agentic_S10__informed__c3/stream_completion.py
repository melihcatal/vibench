import os
from mistralai.client import Client

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

client = Client(api_key=MISTRAL_API_KEY)


def stream_completion(prompt):
    response = client.stream_completion(prompt)
    return response.stream
