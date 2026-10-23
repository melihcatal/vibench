import os
import requests

def check_unsafe_content(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    params = {
        'key': os.getenv('PERSPECTIVE_API_KEY')
    }
    data = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }
    response = requests.post(url, params=params, json=data)
    return response.json()