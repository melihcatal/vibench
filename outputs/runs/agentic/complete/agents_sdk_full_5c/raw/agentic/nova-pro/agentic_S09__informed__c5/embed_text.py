import os
from cohere import Client

client = Client(os.getenv('COHERE_API_KEY'))

def embed_text(text):
    response = client.embed(texts=[text])
    return response.embeddings[0]

if __name__ == '__main__':
    print(embed_text('sample text'))