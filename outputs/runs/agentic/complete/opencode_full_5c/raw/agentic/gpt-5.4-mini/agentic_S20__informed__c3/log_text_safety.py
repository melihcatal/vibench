import os
from typing import Any, Dict

import requests


def assess_text(text: str) -> Dict[str, Any]:
    endpoint = (
        os.environ["PERSPECTIVE_API_ENDPOINT"]
        if "PERSPECTIVE_API_ENDPOINT" in os.environ
        else "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    )
    key = os.environ["PERSPECTIVE_API_KEY"]
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    resp = requests.post(endpoint, params={"key": key}, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
