import os
import requests

def embed_translation_memory(text):
    response = requests.post(
        'https://api.meaningcloud.com/embedding-1.0',
        data={'key': os.getenv('MEANINGCLOUD_API_KEY'), 'txt': text, 'lang': 'en'}
    )
    return response.json()['embeddings'][0]['embedding']