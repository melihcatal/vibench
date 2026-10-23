from __future__ import annotations

import os
from typing import Dict

import requests

from document_models import SafetyCheckResponse


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_content(text: str) -> SafetyCheckResponse:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload: Dict[str, object] = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    params = {"key": api_key}
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return SafetyCheckResponse(unsafe=score >= 0.5, score=score, categories={"TOXICITY": score}, provider="perspective-api")
