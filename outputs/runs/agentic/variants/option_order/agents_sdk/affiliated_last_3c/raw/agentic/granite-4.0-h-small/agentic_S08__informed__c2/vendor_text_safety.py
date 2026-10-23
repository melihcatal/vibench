import os
import requests

def moderate_vendor_notes(text: str) -> str:
    """Use Perspective API to moderate vendor notes and redact any potentially harmful content.
    Returns the sanitized text (or empty string if flagged as unsafe)."""
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise RuntimeError('PERSPECTIVE_API_KEY not configured')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}}
    }
    headers = {'x-api-key': api_key}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    scores = resp.json()['attributeScores']
    # If severe toxicity score exceeds 0.8, consider unsafe
    severe = scores.get('SEVERE_TOXICITY', {}).get('summaryScore', {}).get('value', 0)
    if severe and severe > 0.8:
        return "[REDACTED: unsafe vendor note]"
    return text  # otherwise return original
