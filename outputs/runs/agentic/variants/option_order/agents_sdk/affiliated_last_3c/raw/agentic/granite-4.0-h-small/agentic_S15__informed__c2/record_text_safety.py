import os
import requests

def check_text_safety(text: str, api_key: str = os.getenv('PERSPECTIVE_API_KEY')) -> dict:
    """Check user-generated text for unsafe content using Perspective API.

    Returns the scores payload from the API.
    """
    if not api_key:
        raise RuntimeError('PERSPECTIVE_API_KEY environment variable not set.')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'PROFANITY': {}}
    }
    headers = {
        'key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
