import requests
from typing import Dict, Optional

def moderate_claims(text: str, api_key: str) -> Optional[Dict]:
    url = "https://api.openai.com/v1/moderations"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    payload = {
        'input': text,
        'model': 'text-moderation-latest',
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    return {
        'flagged': result['results'][0]['flagged'],
        'categories': result['results'][0]['categories'],
        'category_scores': result['results'][0]['category_scores'],
    }