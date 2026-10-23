from __future__ import annotations

from typing import Dict

import requests

from security_client import PERSPECTIVE_PROVIDER, get_perspective_config
from security_models import SafetyAssessment


def payload_safety(text: str, language: str = "en") -> Dict[str, object]:
    config = get_perspective_config()
    response = requests.post(
        config["endpoint"],
        params={"key": config["api_key"]},
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in payload.get("attributeScores", {}).items()
    }
    flagged = [name for name, score in scores.items() if score >= 0.7]
    result = SafetyAssessment(
        provider=PERSPECTIVE_PROVIDER,
        model="commentanalyzer.googleapis.com/v1alpha1",
        safe=not flagged,
        scores=scores,
        flagged_categories=flagged,
        raw_response=payload,
    )
    return result.to_dict()
