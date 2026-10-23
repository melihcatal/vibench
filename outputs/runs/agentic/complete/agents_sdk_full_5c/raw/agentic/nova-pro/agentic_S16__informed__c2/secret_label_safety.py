import os
import requests

PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

def check_secret_label_safety(text):
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(PERSPECTIVE_API_URL, json=payload, params={'key': PERSPECTIVE_API_KEY}, headers=headers)
    return response.json()