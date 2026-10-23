import os
from mistralai.client import Client

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

client = Client(api_key=MISTRAL_API_KEY)


def summarize_text(text):
    response = client.summarize(text)
    return response.summary
