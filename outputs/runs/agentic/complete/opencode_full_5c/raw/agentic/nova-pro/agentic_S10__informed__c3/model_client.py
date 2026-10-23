import os
from mistralai.client import Client


def get_client():
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    return Client(api_key=MISTRAL_API_KEY)
