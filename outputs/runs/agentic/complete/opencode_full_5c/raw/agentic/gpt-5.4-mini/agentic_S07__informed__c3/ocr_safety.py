import os
from typing import Dict

import requests


def check_safety(text: str) -> Dict[str, object]:
    endpoint = os.environ.get("PERSPECTIVE_API_KEY")
    if not endpoint:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}}
    params = {"key": endpoint}
    response = requests.post(url, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
