import os
import requests

def transcript_embedding(transcript):
    api_key = os.getenv('GOOGLE_CLOUD_EMBEDDING_API_KEY')
    url = 'https://language.googleapis.com/v1/documents:analyzeEntities?key=' + api_key
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': transcript
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()['entities']