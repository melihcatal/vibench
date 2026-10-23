import os
from cohere import Client


def embed_script(script: str) -> list:
    api_key = os.getenv("COHERE_API_KEY")
    client = Client(api_key=api_key)
    response = client.embed(texts=[script])
    return response.embeddings[0]
