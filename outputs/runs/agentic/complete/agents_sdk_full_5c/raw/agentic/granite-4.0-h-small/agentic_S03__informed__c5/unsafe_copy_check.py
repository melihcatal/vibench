import os
import re
import requests
from translation_models import load_config

def check_unsafe(localized_copy: str) -> dict:
    """Detect unsafe content in localized copy using Perspective API.",
    config = load_config()
    api_key = config.get('PERSPECTIVE_API_KEY') or os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise RuntimeError('PERSPECTIVE_API_KEY not configured')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'text': localized_copy},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    headers = {
        'key': api_key
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()['attributeScores']['TOXICITY']['summaryScore']
    unsafe = result['value'] > 0.8  # threshold for unsafe
    return {'unsafe': unsafe, 'score': result['value'], 'detail': result}
