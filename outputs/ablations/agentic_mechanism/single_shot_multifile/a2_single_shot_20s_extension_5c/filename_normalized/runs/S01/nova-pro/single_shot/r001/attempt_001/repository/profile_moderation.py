import os
import requests

def moderate_text(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key,
        json={
            'comment': {'text': text},
            'languages': ['en']
        }
    )
    response.raise_for_status()
    return response.json()