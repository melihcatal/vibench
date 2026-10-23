import os
import requests
from typing import Tuple, List, Dict, Any

def redact_unsafe(text: str, replace_with: str = "[REDACTED]") -> Tuple[str, List[Dict[str, Any]]]:
    api_key = os.getenv('TISANE_API_KEY')
    if not api_key:
        raise ValueError("TISANE_API_KEY environment variable is required.")
    url = "https://api.tisane.ai/rest/v1/tag/text/en"
    headers = {"apikey": api_key}
    payload = {"content": text}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    violations = data.get('violations', [])
    spans = sorted(violations, key=lambda v: v.get('begin', 0), reverse=True)
    redacted_text = text
    for violation in spans:
        start = violation['begin']
        end = violation['end']
        redacted_text = redacted_text[:start] + replace_with + redacted_text[end:]
    return redacted_text, violations