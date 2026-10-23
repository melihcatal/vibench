import os
import requests
from typing import Dict, Any
from database_models import Document

def check_document_safety(document: Document) -> Dict[str, Any]:
    fields = ['content', 'title', 'description', 'body']
    texts = [document.get(field, '') for field in fields]
    text = ' '.join([t for t in texts if t])
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        return {'error': 'PERSPECTIVE_API_KEY not set'}
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'API request failed', 'status': response.status_code}