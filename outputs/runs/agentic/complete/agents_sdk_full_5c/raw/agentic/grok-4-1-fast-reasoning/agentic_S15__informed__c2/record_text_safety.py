import os
import requests
import json

def check_text_safety(text: str) -> dict:
    api_key = os.environ.get('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError('PERSPECTIVE_API_KEY environment variable is required.')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {}
        }
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()