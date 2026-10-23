import os
import requests
os.environ['PERSPECTIVE_API_KEY'] = 'your_api_key'

def check_safety(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + os.getenv('PERSPECTIVE_API_KEY')
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url, json=payload)
    return response.json()