import os
from typing import Any, Dict

import requests

PERSPECTIVE_API_KEY = os.environ.get('PERSPECTIVE_API_KEY', '')
PERSPECTIVE_HOST = 'commentanalyzer.googleapis.com'
PERSPECTIVE_MODEL = 'TOXICITY'


def moderate_claims(text: str) -> Dict[str, Any]:
    response = requests.post(
        f'https://{PERSPECTIVE_HOST}/v1alpha1/comments:analyze',
        params={'key': PERSPECTIVE_API_KEY},
        json={'comment': {'text': text}, 'requestedAttributes': {PERSPECTIVE_MODEL: {}}},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()
