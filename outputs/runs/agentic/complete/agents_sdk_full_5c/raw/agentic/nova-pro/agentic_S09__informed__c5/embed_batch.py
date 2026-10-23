import os
from cohere import Client

client = Client(os.getenv('COHERE_API_KEY'))

def embed_batch(texts):
    response = client.embed(texts=texts)
    return response.embeddings

if __name__ == '__main__':
    print(embed_batch(['sample text 1', 'sample text 2']))