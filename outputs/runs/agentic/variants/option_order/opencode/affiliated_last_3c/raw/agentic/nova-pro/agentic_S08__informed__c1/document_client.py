import os
from mindee import Client


def get_document_client():
    return Client(api_key=os.getenv("MINDEE_API_KEY"))
