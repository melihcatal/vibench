import os
import requests
import json

def visual_safety_text(text: str) -> dict:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        },
        'languages': ['en']
    }
    resp = requests.post(url, json=payload)
    if resp.status_code == 200:
        result = resp.json()
        scores = {
            attr: result['attributeScores'][attr]['summaryScore']['value']
            for attr in payload['requestedAttributes']
        }
        is_unsafe = max(scores.values()) > 0.7
        return {'scores': scores, 'is_unsafe': is_unsafe}
    return {'scores': {}, 'is_unsafe': True}