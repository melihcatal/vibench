import os
import requests

def embed_transcript(transcript):
    api_key = os.getenv('GOOGLE_CLOUD_LANGUAGE_API_KEY')
    url = f'https://language.googleapis.com/v1/documents:analyzeEntities?key={api_key}'
    data = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': transcript
        },
        'encodingType': 'UTF8'
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()['entities'][0]['name']