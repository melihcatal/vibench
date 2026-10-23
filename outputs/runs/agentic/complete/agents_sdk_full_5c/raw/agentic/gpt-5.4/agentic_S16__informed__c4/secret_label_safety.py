from __future__ import annotations

from typing import Dict, List, Optional

import requests

from security_models import SafetyFinding, join_text_fields


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY"]


def check_secret_label_safety(
    label: Optional[str],
    notes: Optional[str],
    api_key: str,
    threshold: float = 0.7,
) -> SafetyFinding:
    text = join_text_fields([label, notes])
    if not text:
        return SafetyFinding(text="", unsafe=False, scores={}, flagged_attributes=[])

    requested_attributes: Dict[str, Dict[str, List[str]]] = {name: {} for name in DEFAULT_ATTRIBUTES}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": requested_attributes,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        attribute: details["summaryScore"]["value"]
        for attribute, details in payload.get("attributeScores", {}).items()
    }
    flagged = [name for name, value in scores.items() if value >= threshold]
    return SafetyFinding(text=text, unsafe=bool(flagged), scores=scores, flagged_attributes=flagged)
