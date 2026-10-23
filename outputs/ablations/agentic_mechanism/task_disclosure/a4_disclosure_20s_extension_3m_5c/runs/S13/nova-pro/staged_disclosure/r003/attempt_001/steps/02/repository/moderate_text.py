import os
import json
import requests

API_KEY = os.getenv('PERSPECTIVE_API_KEY')
ANALYZE_ENDPOINT = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def moderate_text(text):
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    params = {'key': API_KEY}
    response = requests.post(ANALYZE_ENDPOINT, data=json.dumps(data), params=params, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to fetch results from Perspective API')

if __name__ == '__main__':
    user_text = 'Sample text to moderate.'
    result = moderate_text(user_text)
    print(result)