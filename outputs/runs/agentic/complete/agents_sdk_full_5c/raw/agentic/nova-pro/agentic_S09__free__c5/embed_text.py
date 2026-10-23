import os
from cohere import Client

co = Client(os.getenv('COHERE_API_KEY'))

def embed_text(text):
    response = co.embed(texts=[text])
    return response.embeddings[0]
