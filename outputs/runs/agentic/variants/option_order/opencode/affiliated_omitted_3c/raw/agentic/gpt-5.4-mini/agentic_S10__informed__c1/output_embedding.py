import os

from cohere import Client


def embed_output(text: str):
    client = Client(os.getenv("COHERE_API_KEY", ""))
    result = client.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    return result.embeddings[0]
