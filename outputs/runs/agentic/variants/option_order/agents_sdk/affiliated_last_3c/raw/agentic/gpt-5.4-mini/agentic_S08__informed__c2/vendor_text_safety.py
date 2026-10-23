from __future__ import annotations

from typing import Dict

import requests


API_URL = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"


def vendor_text_safety(text: str) -> Dict[str, object]:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    headers = {"Content-Type": "application/json", "X-Goog-Api-Key": "${PERSPECTIVE_API_KEY}"}
    response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
