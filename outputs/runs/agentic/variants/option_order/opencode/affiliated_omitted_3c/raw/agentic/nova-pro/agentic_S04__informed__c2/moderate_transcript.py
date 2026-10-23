import os
import requests

def moderate_transcript(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze',
        json={
            'comment': {'text': text},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}},
            'key': api_key,
        }
    )
    return response.json()