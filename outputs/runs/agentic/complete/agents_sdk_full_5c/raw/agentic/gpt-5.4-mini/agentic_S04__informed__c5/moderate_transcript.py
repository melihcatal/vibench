from __future__ import annotations

import os
from typing import Dict

import requests


PERSPECTIVE_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(text: str) -> Dict[str, object]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_HOST, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    raise SystemExit("import and call moderate_transcript(text)")
