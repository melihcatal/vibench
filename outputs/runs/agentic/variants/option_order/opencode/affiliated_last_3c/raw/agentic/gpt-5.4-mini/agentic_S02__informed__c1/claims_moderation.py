import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")


def moderate_claims(text: str) -> Dict[str, Any]:
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": PERSPECTIVE_API_KEY},
        json={
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}},
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
