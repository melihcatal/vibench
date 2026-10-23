from __future__ import annotations

import os
from typing import Any, Dict

import requests

from model_models import SafetyCheckRequest, compact_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(request: SafetyCheckRequest) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    text = compact_text(
        "\n".join(filter(None, [request.prompt, request.generated_text]))
    )
    payload = {
        "comment": {"text": text},
        "languages": request.languages or ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
