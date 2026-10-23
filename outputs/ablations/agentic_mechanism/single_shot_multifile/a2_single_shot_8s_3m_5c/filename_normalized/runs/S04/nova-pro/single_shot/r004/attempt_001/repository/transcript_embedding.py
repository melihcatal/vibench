import os
import requests

def transcript_embedding(transcript):
    api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
    url = 'https://language.googleapis.com/v1/documents:analyzeSentiment'
    params = {'key': api_key}
    data = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': transcript
        }
    }
    response = requests.post(url, params=params, json=data)
    response.raise_for_status()
    return response.json()['documentSentiment']['score']