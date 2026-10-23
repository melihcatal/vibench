import os
import requests

PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
PERSPECTIVE_API_KEY = os.environ.get('PERSPECTIVE_API_KEY', '')


def check_ocr_text_safety(text: str) -> dict:
    params = {'key': PERSPECTIVE_API_KEY}
    payload = {'comment': {'text': text}, 'languages': ['en'], 'requestedAttributes': {'TOXICITY': {}}}
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
