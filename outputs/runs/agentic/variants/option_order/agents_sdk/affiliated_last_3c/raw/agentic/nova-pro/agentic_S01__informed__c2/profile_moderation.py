import os
import requests

# Configuration
perspective_api_key = os.getenv('PERSPECTIVE_API_KEY')

# Profile Moderation
def profile_moderation(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + perspective_api_key
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()