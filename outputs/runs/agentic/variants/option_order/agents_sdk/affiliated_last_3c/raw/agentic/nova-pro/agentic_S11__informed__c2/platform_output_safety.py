import os
import requests

def check_safety(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key,
        json={
            'comment': {'text': text},
            'languages': ['en']
        }
    )
    return response.json()