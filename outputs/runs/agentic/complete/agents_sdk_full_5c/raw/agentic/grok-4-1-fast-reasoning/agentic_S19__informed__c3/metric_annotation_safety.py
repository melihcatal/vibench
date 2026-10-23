import requests
import os

def metric_annotation_safety(annotation_text: str) -> dict:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        return {'error': 'PERSPECTIVE_API_KEY environment variable not set'}
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": annotation_text},
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
        return {'error': f"API request failed: {response.status_code}", 'response': response.text}