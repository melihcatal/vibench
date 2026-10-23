import os
import requests

def moderate_claims(claims):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'comment': {'text': claims},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
        'doNotStore': True
    }
    response = requests.post(url, headers=headers, json=payload, params={'key': api_key})
    return response.json()

if __name__ == '__main__':
    claims = 'example claim'
    print(moderate_claims(claims)