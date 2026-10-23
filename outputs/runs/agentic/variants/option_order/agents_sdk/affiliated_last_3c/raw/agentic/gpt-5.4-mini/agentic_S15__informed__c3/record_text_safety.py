from __future__ import annotations

from typing import Dict

import requests

from database_models import OperationResponse

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_record_safety(text: str) -> OperationResponse:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": __import__("os").environ.get("PERSPECTIVE_API_KEY", "")},
        json={
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    data: Dict = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return OperationResponse(ok=score < 0.7, message=f"toxicity={score:.3f}")
