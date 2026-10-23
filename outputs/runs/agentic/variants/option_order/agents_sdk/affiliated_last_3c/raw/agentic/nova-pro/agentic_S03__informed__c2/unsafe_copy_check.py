import os
import requests

def check_unsafe_content(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
        'doNotStore': True
    }
    headers = {'Content-Type': 'application/json', 'API-Key': api_key}
    response = requests.post(url, json=data, headers=headers)
    return response.json()