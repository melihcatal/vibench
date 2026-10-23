import os
from cohere import Client

def get_embeddings_client() -&gt; Client:
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        raise ValueError('COHERE_API_KEY environment variable is required.')
    return Client(api_key)