from __future__ import annotations

from typing import Dict

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def vendor_text_safety(text: str) -> Dict[str, object]:
    api_key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    resp = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=30)
    resp.raise_for_status()
    return {"provider": "perspective-api", "raw": resp.json()}
