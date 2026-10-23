import requests
import os

def check_annotation_safety(text: str):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {'key': api_key}
    headers = {'Content-Type': 'application/json'}
    data = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }

    response = requests.post(url, params=params, headers=headers, json=data)
    response.raise_for_status() # Raise an exception for HTTP errors
    return response.json()

