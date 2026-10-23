import os
import requests

API_KEY = os.getenv('PERSPECTIVE_API_KEY')
URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + API_KEY

def moderate_claims(claims):
    payload = {
        'comment': {'text': claims},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(URL, json=payload)
    return response.json()