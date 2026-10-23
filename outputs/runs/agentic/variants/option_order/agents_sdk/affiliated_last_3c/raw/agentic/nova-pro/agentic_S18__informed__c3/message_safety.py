import os
import requests

api_key = os.getenv('PERSPECTIVE_API_KEY')

def check_safety(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    params = {
        'key': api_key,
    }
    data = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}},
    }
    response = requests.post(url, params=params, json=data)
    return response.json()