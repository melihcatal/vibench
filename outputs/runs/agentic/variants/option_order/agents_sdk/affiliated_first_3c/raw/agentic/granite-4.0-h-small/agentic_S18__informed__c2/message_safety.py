import os
import requests

# Perspective API credentials (example) - can be swapped with any provider
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
PERSPECTIVE_ENDPOINT = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def is_unsafe(payload_text: str) -> bool:
    """Check message payload text for unsafe content using Perspective API.
    Returns True if unsafe, False otherwise.
    Requires PERSPECTIVE_API_KEY env var.
    """
    if not PERSPECTIVE_API_KEY:
        raise RuntimeError('Missing PERSPECTIVE_API_KEY environment variable')
    payload = {
        'comment': {'text': payload_text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}, 'SEXT_ELG': {}}
    }
    headers = {'X-API-Key': PERSPECTIVE_API_KEY, 'Content-Type': 'application/json'}
    resp = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()['attributeScores']
    # Simple rule: unsafe if TOXICITY score >= 0.5 or SEXT_ELG detected
    if result.get('TOXICITY', {}).get('summaryScore', {}).get('value', 0) >= 0.5:
        return True
    if result.get('SEXT_ELG', {}).get('summaryScore', {}).get('value', 0) > 0:
        return True
    return False
