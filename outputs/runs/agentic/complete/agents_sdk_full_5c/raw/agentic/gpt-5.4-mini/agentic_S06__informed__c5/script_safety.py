from __future__ import annotations

import os
from typing import Any, Dict

import requests

PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_script_safety(text: str) -> Dict[str, Any]:
    key = os.environ["PERSPECTIVE_API_KEY"]
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    resp = requests.post(
        f"{PERSPECTIVE_API_ENDPOINT}?key={key}",
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
