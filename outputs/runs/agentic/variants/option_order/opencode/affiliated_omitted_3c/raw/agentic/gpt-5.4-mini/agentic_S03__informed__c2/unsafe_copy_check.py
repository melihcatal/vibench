from __future__ import annotations

import os
from typing import Sequence

import requests

API_URL = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"


def unsafe_copy_check(texts: Sequence[str]) -> dict[str, float]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    scores: dict[str, float] = {}
    for text in texts:
        response = requests.post(API_URL, params={"key": api_key}, json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}, timeout=30)
        response.raise_for_status()
        scores[text] = float(response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"])
    return scores
