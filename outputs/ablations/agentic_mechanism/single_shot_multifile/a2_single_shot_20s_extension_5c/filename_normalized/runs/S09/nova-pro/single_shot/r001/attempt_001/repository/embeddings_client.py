import os
import requests

class EmbeddingsClient:
    def __init__(self):
        self.api_key = os.getenv('DIRECT_EMBEDDINGS_API_KEY')
        self.api_url = 'https://api.directembeddings.com/v1/embed'

    def generate_embedding(self, text):
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        payload = {'text': text,'model': 'direct-embeddings-v1'}
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['embedding']

    def generate_batch_embeddings(self, texts):
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        payload = {'texts': texts,'model': 'direct-embeddings-v1'}
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['embeddings']