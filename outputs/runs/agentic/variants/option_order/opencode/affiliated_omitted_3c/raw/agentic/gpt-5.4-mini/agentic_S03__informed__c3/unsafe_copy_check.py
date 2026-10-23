import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'


def check_unsafe_copy(text: str) -> Dict[str, Any]:
    params = {'key': os.environ.get('PERSPECTIVE_API_KEY', '')}
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'INSULT': {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
