import os
import requests
from typing import List, Dict, Any

def corpus_safety(corpus: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError('PERSPECTIVE_API_KEY environment variable is required.')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    results = []
    for text in corpus:
        payload = {
            'comment': {'text': text},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'INSULT': {},
                'PROFANITY': {},
                'THREAT': {}
            }
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            scores = response.json()['attributeScores']
            score_values = {k: v['summaryScore']['value'] for k, v in scores.items()}
            is_safe = all(value < 0.5 for value in score_values.values())
            results.append({
                'text_preview': text[:50] + '...' if len(text) > 50 else text,
                'is_safe': is_safe,
                'scores': score_values
            })
        else:
            results.append({'text_preview': text[:50] + '...', 'is_safe': False, 'error': 'API error'})
    return results
