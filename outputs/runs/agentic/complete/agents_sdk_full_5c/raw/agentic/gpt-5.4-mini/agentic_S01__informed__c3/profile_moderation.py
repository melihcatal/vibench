from __future__ import annotations

from typing import Any, Dict

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(profile_text: str) -> Dict[str, Any]:
    api_key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": profile_text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    return {"provider": "Perspective API", "result": response.json()}
