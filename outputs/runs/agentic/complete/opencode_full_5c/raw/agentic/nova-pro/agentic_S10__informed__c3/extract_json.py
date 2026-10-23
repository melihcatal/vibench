import os
from mistralai.client import Client

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

client = Client(api_key=MISTRAL_API_KEY)


def extract_json(text):
    response = client.extract_json(text)
    return response.json
