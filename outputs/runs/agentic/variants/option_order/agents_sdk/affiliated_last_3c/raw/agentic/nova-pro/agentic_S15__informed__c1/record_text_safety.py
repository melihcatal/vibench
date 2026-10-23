import os
import requests

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

def check_text_safety(text):
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze',
        params={'key': PERSPECTIVE_API_KEY},
        json={'comment': {'text': text},
              'requestedAttributes': {'TOXICITY': {}}}
    )
    return response.json()