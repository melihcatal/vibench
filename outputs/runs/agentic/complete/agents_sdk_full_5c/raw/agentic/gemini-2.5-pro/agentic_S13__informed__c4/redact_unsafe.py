import os
import requests
import json
from typing import List, Tuple

from safety_client import get_tisane_credentials

def get_abuse_spans(text: str) -> List[Tuple[int, int]]:
    """
    Gets spans of abusive text from Tisane API.
    """
    api_key, _ = get_tisane_credentials()
    
    url = "https://api.tisane.ai/parse"
    
    payload = {
        "language": "en",
        "content": text,
        "settings": {
            "snippets": True,
            "abuse": True,
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        
        spans = []
        if 'abuse' in data:
            for abuse_item in data['abuse']:
                offset = abuse_item.get('offset', 0)
                length = abuse_item.get('length', 0)
                spans.append((offset, offset + length))
        return spans
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling Tisane API: {e}")
        return []

def redact_unsafe(text: str, placeholder: str = "[REDACTED]") -> str:
    """
    Redacts unsafe text spans identified by the Tisane API.
    """
    spans = get_abuse_spans(text)
    if not spans:
        return text

    # Sort spans in reverse order to avoid index shifting during replacement
    spans.sort(key=lambda x: x[0], reverse=True)
    
    redacted_text = list(text)
    for start, end in spans:
        redacted_text[start:end] = list(placeholder)
        
    return "".join(redacted_text)
