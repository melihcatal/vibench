import os
import requests
from database_models import normalize_item

def check_safety(document_id: str, raw_item: dict) -> bool:
    """Check user‑generated text fields for unsafe content using Tisane API.
    Returns True if safe, False otherwise.
    """
    # Normalize to plain Python types
    item = normalize_item(raw_item)
    # Identify text fields that may contain user content (configurable)
    text_fields = ['title', 'content', 'description', 'comments']
    texts = [str(item.get(f)) for f in text_fields if f in item]
    if not texts:
        return True  # nothing to check
    # Tisane endpoint (example URL)
    endpoint = 'https://api.tisane.ai/v1/parse'
    api_key = os.getenv('TISANE_API_KEY')
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'language': 'en', 'text': ' '.join(texts)}
    response = requests.post(endpoint, headers=headers, json=payload, timeout=5)
    if response.status_code != 200:
        raise RuntimeError(f'Tisane API error: {response.status_code} {response.text}')
    result = response.json()
    # Tisane returns a 'issues' list; empty means safe
    return not result.get('issues')
