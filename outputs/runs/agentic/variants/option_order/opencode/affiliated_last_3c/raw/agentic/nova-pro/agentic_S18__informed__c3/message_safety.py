import os
import requests

# Perspective API configuration
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

def check_safety(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    params = {
        'key': PERSPECTIVE_API_KEY
    }
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url, params=params, json=data)
    return response.json()

if __name__ == '__main__':
    text = 'Hello, world!'
    safety_check = check_safety(text)
    print(f'Safety check result: {safety_check}