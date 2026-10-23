# ocr_safety.py
import os
import requests
from typing import Any, Dict

# Local helpers
from document_models import OCRResult

# Perspective API endpoint (REST)
PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

# Placeholder for your Perspective API key
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')


def _send_perspective(payload: Dict[str, Any]) -> Any:
    """Internal helper that sends a request to Perspective API and returns parsed JSON."""
    if not PERSPECTIVE_API_KEY:
        raise RuntimeError('Set PERSPECTIVE_API_KEY environment variable for safety checks')
    headers = {'content-type': 'application/json', 'x-guest-token': PERSPECTIVE_API_KEY}
    response = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def check_toxicity(text: str, context: Dict[str, str] = None) -> Dict[str, Any]:
    """Call Perspective API to assess toxicity / aggression."""
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}, 'AGGRESSION': {}}
    }
    if context:
        payload['context'] = context
    response = _send_perspective(payload)
    return response


def is_unsafe(text: str, threshold: float = 0.9) -> bool:
    """Return True if toxicity/ aggression score exceeds the threshold."""
    scores = check_toxicity(text)
    # Example scoring path: response['attributeScores']['TOXICITY']['summaryScore']['value']
    toxicity = scores['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity >= threshold

# Example demo (remove when integrated)
if __name__ == '__main__':
    demo_text = 'This looks like a hateful comment for testing purposes.'
    print('Unsafe?', is_unsafe(demo_text, threshold=0.8))
    print('Detailed scores:', check_toxicity(demo_text))