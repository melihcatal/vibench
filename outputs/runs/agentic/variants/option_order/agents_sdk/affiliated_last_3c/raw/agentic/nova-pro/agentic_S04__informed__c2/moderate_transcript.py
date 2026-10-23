import os
import requests

def moderate_transcript(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    response = requests.post(URL, json=data)
    return response.json()