import os
import requests
from typing import Dict, Any

def ocr_safety(text: str) -> Dict[str, Any]:
    """
    Check extracted document text for unsafe content using Perspective API.
    """
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANE': {},
            'IDENTITY_ATTACK': {}
        },
        'languages': ['en']
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
