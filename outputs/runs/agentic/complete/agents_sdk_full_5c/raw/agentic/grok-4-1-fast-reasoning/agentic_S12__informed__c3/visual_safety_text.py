import os
import requests
import json
from typing import Dict, Any
from vision_models import ImageLabels, ImageSafety

PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
api_key = os.getenv('PERSPECTIVE_API_KEY')

def visual_safety_text(labels: ImageLabels) -> ImageSafety:
    texts = [label['name'] for label in labels['labels']]
    risks = []
    scores = {}
    for text in texts:
        if len(text) < 3:
            continue
        data = {
            'comment': {'text': text},
            'requestedAttributes': {'TOXICITY': {}, 'INSULT': {}, 'PROFANE': {}, 'HATE': {}}
        }
        params = {'key': api_key}
        resp = requests.post(PERSPECTIVE_API_URL, params=params, json=data)
        if resp.status_code == 200:
            result = resp.json()
            for attr, score_data in result['attributeScores'].items():
                score_key = f"{text[:20]}:{attr}"
                score = score_data['summaryScore']['value']
                scores[score_key] = score
                if score > 0.7:
                    risks.append(f"{text} ({attr})")
    is_safe = len(risks) == 0
    return {'is_safe': is_safe, 'risks': risks, 'scores': scores}