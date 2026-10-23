import os
from cohere import Client

def embed_text(text):
    client = Client(os.getenv('COHERE_API_KEY'))
    response = client.embed(texts=[text])
    return response.embeddings[0]