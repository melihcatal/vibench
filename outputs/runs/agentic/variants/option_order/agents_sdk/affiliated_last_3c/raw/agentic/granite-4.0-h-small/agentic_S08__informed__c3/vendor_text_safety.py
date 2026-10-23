import os
import requests

# Perspective API - concrete provider identified by endpoint
PERSPECTIVE_ENDPOINT = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

API_KEY = os.getenv('PERSPECTIVE_API_KEY')
HEADERS = {'content-type': 'application/json', 'x-agnostic-api-key': API_KEY}

def moderate_vendor_notes(notes):
    '''Moderate vendor notes using Perspective API to detect toxicity.
    Returns a tuple (is_safe, score). Safe if score < 0.5 (custom threshold).
    '''
    payload = {
        'comment': {'text': notes},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=HEADERS)
    data = response.json()
    score = data['attributeScores']['TOXICITY']['summaryScore']['value']
    is_safe = score < 0.5
    return is_safe, score
