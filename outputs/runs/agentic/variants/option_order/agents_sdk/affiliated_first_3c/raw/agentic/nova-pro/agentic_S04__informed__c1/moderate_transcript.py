import os
import requests

def moderate_transcript(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    headers = {'Content-Type': 'application/json'}
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {} }
    }
    response = requests.post(url, headers=headers, params={'key': api_key}, json=data)
    return response.json()