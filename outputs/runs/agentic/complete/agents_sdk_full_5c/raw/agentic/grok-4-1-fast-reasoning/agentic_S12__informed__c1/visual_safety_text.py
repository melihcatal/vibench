"""[LATER-STEP] Check generated visual labels for unsafe text"""
import requests
from vision_client import get_api_key
from vision_models import SafetyResponse
from typing import List

def visual_safety_text(texts: List[str]) -> SafetyResponse:
    # Perspective API
    key = get_api_key('PERSPECTIVE_API_KEY')
    text = ' '.join(texts)
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANE': {},
            'SEXUALLY_EXPLICIT': {}
        },
        'languages': ['en']
    }
    response = requests.post(url, json=payload).json()
    scores = response['attributeScores']
    risks = [attr for attr, score in scores.items() if score['summaryScore']['value'] > 0.5]
    is_safe = len(risks) == 0
    return {'is_safe': is_safe, 'risks': risks}
