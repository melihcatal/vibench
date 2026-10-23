import os
import requests

class DirectEmbeddingsClient:
    def __init__(self):
        self.api_key = os.getenv('DIRECT_EMBEDDINGS_API_KEY')
        self.api_url = 'https://api.directembeddings.com/v1/embed'

    def generate_embedding(self, text):
        response = requests.post(self.api_url, headers={'Authorization': f'Bearer {self.api_key}'}, json={'text': text})
        response.raise_for_status()
        return response.json()['embedding']

    def generate_batch_embeddings(self, texts):
        response = requests.post(self.api_url, headers={'Authorization': f'Bearer {self.api_key}'}, json={'texts': texts})
        response.raise_for_status()
        return response.json()['embeddings']