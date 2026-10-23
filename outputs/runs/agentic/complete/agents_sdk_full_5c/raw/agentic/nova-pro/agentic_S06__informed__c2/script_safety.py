import os
import requests

def check_safety(text):
    api_url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    params = {
        'key': os.environ.get('PERSPECTIVE_API_KEY'),
    }
    data = {
        'comment': {'text': text},
        'languages': ['en']
    }
    response = requests.post(api_url, params=params, json=data)
    return response.json()