import os
import requests

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

def check_safety(text):
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze',
        json={
            'comment': {'text': text},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}},
            'key': PERSPECTIVE_API_KEY
        }
    )
    return response.json()['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5