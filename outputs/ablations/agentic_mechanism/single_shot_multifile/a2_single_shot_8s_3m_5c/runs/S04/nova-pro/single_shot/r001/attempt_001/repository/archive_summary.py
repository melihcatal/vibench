import os
import requests

def summarize_transcript(transcript):
    api_key = os.getenv('GOOGLE_CLOUD_LANGUAGE_API_KEY')
    url = 'https://language.googleapis.com/v1/documents:analyzeEntities'
    payload = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': transcript
        },
        'encodingType': 'UTF8'
    }
    headers = {'Content-Type': 'application/json'}
    params = {'key': api_key}
    response = requests.post(url, json=payload, params=params, headers=headers)
    entities = response.json().get('entities', [])
    summary = ' '.join([entity['name'] for entity in entities])
    return summary