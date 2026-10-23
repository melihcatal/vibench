import os
import requests

def check_safety(text):
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze',
        json={
            'comment': {'text': text},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}},
        params={'key': os.getenv('PERSPECTIVE_API_KEY')}
    )
    return response.json()