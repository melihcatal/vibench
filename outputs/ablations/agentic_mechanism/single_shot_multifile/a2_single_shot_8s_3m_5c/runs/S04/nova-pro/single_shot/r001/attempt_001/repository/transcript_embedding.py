import os
import requests

def embed_transcript(transcript):
    api_key = os.getenv('SENTENCE_TRANSFORMERS_API_KEY')
    url = 'https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {'inputs': transcript}
    response = requests.post(url, headers=headers, json=payload)
    embeddings = response.json()
    return embeddings