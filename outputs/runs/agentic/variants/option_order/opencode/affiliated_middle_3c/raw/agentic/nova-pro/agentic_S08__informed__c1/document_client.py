import os
from mindee import Client


def get_client():
    api_key = os.getenv("MINDEE_API_KEY")
    return Client(api_key)
