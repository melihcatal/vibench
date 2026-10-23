import os
import requests

os.environ["PERSPECTIVE_API_KEY"] = "your-perspective-api-key"

def check_safety(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    params = {
        'key': os.getenv('PERSPECTIVE_API_KEY')
    }
    data = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url, params=params, json=data)
    return response.json()