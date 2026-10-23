import os
from typing import List, Dict
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def summarize_translation_quality(source_texts: List[str], target_texts: List[str]) -> Dict[str, int]:
    """Summarize translation quality issues using Perspective API.
    Returns a dictionary counting each issue type found in the translated text.
    """
    # Perspective API endpoint (REST) - uses HTTP POST with JSON payload
    PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    API_KEY = os.getenv('PERSPECTIVE_API_KEY')
    if not API_KEY:
        raise RuntimeError('PERSPECTIVE_API_KEY environment variable not set')

    # Simple scoring request for toxicity
    def _score(content: str) -> float:
        import json, requests
        payload = {
            'comment': {'text': content},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}
        }
        headers = {'Content-Type': 'application/json', 'x-api-key': API_KEY}
        resp = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        attrib = resp.json().get('attributeScores', {}).get('TOXICITY', {}).get('summaryScore', {})
        return attrib.get('value', 0.0)

    scores = {'toxic': 0, 'severe_toxic': 0, 'other': 0}
    for src, tgt in zip(source_texts, target_texts):
        toxicity = _score(tgt)
        if toxicity >= 0.9:
            scores['severe_toxic'] += 1
        elif toxicity >= 0.5:
            scores['toxic'] += 1
        else:
            scores['other'] += 1
    return scores
