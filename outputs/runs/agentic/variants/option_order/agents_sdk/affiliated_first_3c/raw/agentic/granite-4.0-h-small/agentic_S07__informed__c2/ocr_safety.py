import os
import requests

API_KEY = os.getenv('PERSPECTIVE_API_KEY')
URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def check_for_unsafe(text: str) -> dict:
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}, 'SEXY': {}}
    }
    headers = {'x-api-key': API_KEY}
    resp = requests.post(URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()
