import os
import requests

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

def moderate_claims(claims):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'comment': claims,
        'languages': ['en']
    }
    response = requests.post('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + PERSPECTIVE_API_KEY, headers=headers, json=payload)
    moderation_result = response.json()
    print(moderation_result)