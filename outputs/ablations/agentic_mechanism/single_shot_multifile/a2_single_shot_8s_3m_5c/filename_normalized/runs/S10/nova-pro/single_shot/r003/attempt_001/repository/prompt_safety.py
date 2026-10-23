import os
import requests

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

def check_safety(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + PERSPECTIVE_API_KEY
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
       'requestedAttributes': {'TOXICITY': {}},
    }
    response = requests.post(url, json=payload)
    return response.json()['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5