import os
from cohere import Client

cohere_client = Client(os.getenv('COHERE_API_KEY'))

def embed_text(text):
    response = cohere_client.embed(texts=[text])
    return response.embeddings[0]