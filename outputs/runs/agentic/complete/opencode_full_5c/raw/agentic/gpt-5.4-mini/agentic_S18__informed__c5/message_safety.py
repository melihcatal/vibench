import os
import requests

def check_message_safety(text):
    key = os.environ['PERSPECTIVE_API_KEY']
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {'comment': {'text': text}, 'requestedAttributes': {'TOXICITY': {}}, 'doNotStore': True, 'languages': ['en']}
    response = requests.post(url, params={'key': key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
