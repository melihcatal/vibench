from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def platform_output_safety(text: str, language: str = "en") -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in payload.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective_api",
        "scores": scores,
        "raw": payload,
    }
