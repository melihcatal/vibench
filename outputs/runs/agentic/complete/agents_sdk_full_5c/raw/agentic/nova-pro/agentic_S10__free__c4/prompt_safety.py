import os
import requests

perspective_api_key = os.getenv('PERSPECTIVE_API_KEY')

def check_safety(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + perspective_api_key
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url, json=payload)
    return response.json()