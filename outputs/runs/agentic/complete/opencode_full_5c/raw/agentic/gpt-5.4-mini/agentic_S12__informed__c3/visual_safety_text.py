from typing import Any, Dict, List

import requests


API_URL = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"


def visual_safety_text(text: str, api_key: str) -> Dict[str, Any]:
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    r = requests.post(API_URL, params={"key": api_key}, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
