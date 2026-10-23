import os
import requests
from typing import List, Dict, Any

TISANE_API_KEY = os.getenv("TISANE_API_KEY")
BASE_URL = "https://api.tisane.ai/v1"

def _get_headers() -&gt; Dict[str, str]:
    return {
        "Api-Key": TISANE_API_KEY,
        "Content-Type": "application/json"
    }

def moderate_text(text: str, language: str = "auto") -&gt; Dict[str, Any]:
    payload = {"content": text, "language": language}
    response = requests.post(f"{BASE_URL}/moderate", json=payload, headers=_get_headers())
    response.raise_for_status()
    return response.json()

def moderate_batch(texts: List[str], language: str = "auto") -&gt; List[Dict[str, Any]]:
    return [moderate_text(text, language) for text in texts]

def redact_text(text: str) -&gt; Dict[str, Any]:
    payload = {"content": text}
    response = requests.post(f"{BASE_URL}/redact", json=payload, headers=_get_headers())
    response.raise_for_status()
    return response.json()