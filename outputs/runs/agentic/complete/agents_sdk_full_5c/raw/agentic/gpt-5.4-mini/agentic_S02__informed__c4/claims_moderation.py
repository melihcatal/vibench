from __future__ import annotations

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_claim_text(text: str) -> dict:
    resp = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": __import__("os").environ.get("PERSPECTIVE_API_KEY", "")},
        json={
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}},
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()
