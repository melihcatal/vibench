import os
import requests
import json

def ocr_safety(text: str, threshold: float = 0.5) -> bool:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url, json=payload)
    data = response.json()
    toxicity_score = data['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score < threshold