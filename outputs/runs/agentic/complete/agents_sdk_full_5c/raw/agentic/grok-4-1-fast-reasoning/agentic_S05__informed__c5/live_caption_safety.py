import os
import requests
from typing import Dict, Any

def check_live_caption_safety(caption: str) -> Dict[str, Any]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        return {'error': 'PERSPECTIVE_API_KEY not set'}
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': caption},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        },
        'languages': ['en']
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
