import os
import requests
import json
from typing import Dict

def moderate_profile_text(text: str) -&gt; Dict[str, Any]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
        },
        "languages": ["en"]
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    scores = data['attributeScores']
    return {
        'toxicity': scores['TOXICITY']['summaryScore']['value'],
        'severe_toxicity': scores['SEVERE_TOXICITY']['summaryScore']['value'],
        'insult': scores['INSULT']['summaryScore']['value'],
        'profanity': scores['PROFANITY']['summaryScore']['value'],
        'is_safe': scores['TOXICITY']['summaryScore']['value'] &lt; 0.5,
    }