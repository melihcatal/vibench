from __future__ import annotations

from typing import Any, Dict, Iterable

import requests

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com"
PERSPECTIVE_API_VERSION = "v1alpha1"


def check_text_safety(text: str, api_key: str) -> Dict[str, Any]:
    response = requests.post(
        f"{PERSPECTIVE_API_HOST}/{PERSPECTIVE_API_VERSION}/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
