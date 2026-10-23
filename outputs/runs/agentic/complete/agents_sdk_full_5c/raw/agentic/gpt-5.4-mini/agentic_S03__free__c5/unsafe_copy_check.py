import os
from typing import Dict

import requests


PERSPECTIVE_API_KEY_ENV = "PERSPECTIVE_API_KEY"
PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_copy(text: str) -> Dict[str, float]:
    api_key = os.getenv(PERSPECTIVE_API_KEY_ENV, "")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(f"{PERSPECTIVE_API_HOST}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    attributes = response.json().get("attributeScores", {})
    return {name: values["summaryScore"]["value"] for name, values in attributes.items() if "summaryScore" in values}
