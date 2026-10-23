import os
import requests

def check_text_safety(text):
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze',
        params={'key': os.getenv('PERSPECTIVE_API_KEY')},
        json={
            'comment': {'text': text},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}},
        }
    )
    return response.json()