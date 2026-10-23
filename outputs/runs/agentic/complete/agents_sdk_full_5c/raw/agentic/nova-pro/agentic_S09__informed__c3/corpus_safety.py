import os
import requests

PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def check_corpus_safety(text):
    params = {
        'key': os.getenv('PERSPECTIVE_API_KEY'),
    }
    data = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=data)
    return response.json()