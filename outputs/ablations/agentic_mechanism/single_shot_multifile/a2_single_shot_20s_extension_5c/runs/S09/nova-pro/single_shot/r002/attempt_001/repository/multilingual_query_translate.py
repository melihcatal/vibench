import os
import requests

def translate_query(query, target_language):
    api_key = os.getenv('DIRECT_EMBEDDINGS_API_KEY')
    api_url = 'https://api.directembeddings.com/v1/translate'
    response = requests.post(api_url, headers={'Authorization': f'Bearer {api_key}'}, json={'text': query, 'target_language': target_language})
    response.raise_for_status()
    return response.json()['translated_text']