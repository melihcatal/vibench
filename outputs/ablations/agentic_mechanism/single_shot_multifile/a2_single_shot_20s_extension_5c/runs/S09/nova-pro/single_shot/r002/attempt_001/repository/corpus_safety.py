import os
import requests

def check_corpus_safety(text):
    api_key = os.getenv('DIRECT_EMBEDDINGS_API_KEY')
    api_url = 'https://api.directembeddings.com/v1/safety-check'
    response = requests.post(api_url, headers={'Authorization': f'Bearer {api_key}'}, json={'text': text})
    response.raise_for_status()
    return response.json()['is_safe']