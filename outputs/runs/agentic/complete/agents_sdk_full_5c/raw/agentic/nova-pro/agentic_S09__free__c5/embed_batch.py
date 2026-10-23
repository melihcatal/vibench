import os
from cohere import Client

co = Client(os.getenv('COHERE_API_KEY'))

def embed_batch(texts):
    response = co.embed(texts=texts)
    return response.embeddings
