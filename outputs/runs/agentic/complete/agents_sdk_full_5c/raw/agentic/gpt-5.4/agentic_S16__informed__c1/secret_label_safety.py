from __future__ import annotations

import os
from typing import Dict, Iterable, List

import requests

from security_client import get_secret_metadata
from security_models import SafetyFinding


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT", "PROFANITY")


def _moderate_text(text: str) -> SafetyFinding:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores: Dict[str, float] = {
        name: payload["attributeScores"][name]["summaryScore"]["value"]
        for name in DEFAULT_ATTRIBUTES
        if name in payload.get("attributeScores", {})
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return SafetyFinding(text=text, flagged=flagged, categories=scores)


def check_secret_labels_and_notes(secret_id: str, project_id: str | None = None, notes: str = "") -> List[SafetyFinding]:
    metadata = get_secret_metadata(secret_id=secret_id, project_id=project_id)
    findings: List[SafetyFinding] = []
    label_texts: Iterable[str] = [f"{k}:{v}" for k, v in dict(metadata.labels).items()]
    for text in label_texts:
        findings.append(_moderate_text(text))
    if notes.strip():
        findings.append(_moderate_text(notes))
    return findings
