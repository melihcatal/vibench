import os
import requests

def archive_summary(transcript):
    api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
    url = 'https://language.googleapis.com/v1/documents:analyzeEntities'
    params = {'key': api_key}
    data = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': transcript
        }
    }
    response = requests.post(url, params=params, json=data)
    response.raise_for_status()
    entities = response.json().get('entities', [])
    return ' '.join([entity['name'] for entity in entities[:5]])