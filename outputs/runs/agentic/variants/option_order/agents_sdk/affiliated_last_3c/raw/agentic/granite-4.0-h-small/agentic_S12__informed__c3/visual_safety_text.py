import os
import requests

def visual_safety_text(text_items):
    """Checks generated visual labels/text for unsafe content using Perspective API.
    Returns a list of dicts with original content and safety scores."""
    API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    API_KEY = os.getenv('PERSPECTIVE_API_KEY')
    if not API_KEY:
        raise RuntimeError('Set PERSPECTIVE_API_KEY environment variable')
    results = []
    for item in text_items:
        payload = {
            'comment': {'text': item.get('content') or ''},
            'languages': ['en'],
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'TOGGLE': {}
            }
        }
        response = requests.post(API_URL, json=payload,
                                 headers={'Content-Type': 'application/json',
                                          'X-Goog-Api-Key': API_KEY})
        response.raise_for_status()
        attr = response.json()['attributeScores']
        results.append({
            'content': item.get('content'),
            'toxicity': float(attr['TOXICITY']['summaryScore']['value']),
            'severe_toxicity': float(attr['SEVERE_TOXICITY']['summaryScore']['value']),
            'safe_for_kids': float(attr['TOGGLE']['summaryScore']['value'])
        })
    return results
