import os
import requests

PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def check_text_safety(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    response = requests.post(
        PERSPECTIVE_API_URL,
        json={
            'comment': {'text': text},
            'requestedAttributes': {'TOXICITY': {}},
            'languages': ['en']
        },
        params={'key': api_key}
    )
    return response.json()['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5