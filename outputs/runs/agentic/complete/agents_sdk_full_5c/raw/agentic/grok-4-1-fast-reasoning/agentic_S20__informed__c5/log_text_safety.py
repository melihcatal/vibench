import requests
import os
from typing import Dict, Any

def check_log_safety(text: str) -> Dict[str, Any]:
    """
    Check selected log message text for unsafe content using Perspective API.
    """
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()['attributeScores']
