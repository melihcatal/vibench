import os
import requests
from typing import Dict, Any

def unsafe_copy_check(text: str) -> Dict[str, Any]:
    \"\"\"
    Check localized copy for unsafe content using Google Perspective API.
    \"\"\"
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError('PERSPECTIVE_API_KEY environment variable is required.')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
            'IDENTITY_ATTACK': {}
        },
        'languages': ['en']
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()