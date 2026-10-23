import argparse
import json
import os
import requests
from typing import List, Dict

def check_visual_safety_text(texts: List[str]) -> Dict[str, float]:
    text = ' '.join(texts)
    if not text.strip():
        return {}
    api_key = os.environ['PERSPECTIVE_API_KEY']
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'INSULT': {},
            'PROFANITY': {},
            'IDENTITY_ATTACK': {}
        }
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    scores = response.json()['attributeScores']
    return {k: scores[k]['summaryScore']['value'] for k in scores}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check text safety using Perspective API')
    parser.add_argument('texts_json', help='JSON list of texts, e.g. ["text1", "text2"]')
    args = parser.parse_args()
    texts = json.loads(args.texts_json)
    result = check_visual_safety_text(texts)
    print(json.dumps(result, indent=2))