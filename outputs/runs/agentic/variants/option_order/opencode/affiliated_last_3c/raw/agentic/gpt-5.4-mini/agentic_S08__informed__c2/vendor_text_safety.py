from typing import Any, Dict
import requests
from document_client import require_env


def vendor_text_safety(text: str) -> Dict[str, Any]:
    api_key = require_env('PERSPECTIVE_API_KEY')
    response = requests.post('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze', params={'key': api_key}, json={'comment': {'text': text}, 'requestedAttributes': {'TOXICITY': {}}}, timeout=60)
    data = response.json()
    return {'provider': 'perspective', 'raw': data}
