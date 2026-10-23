# [LATER-STEP] vendor_text_safety.py
# Moderate vendor notes or memo fields using Perspective API

import os
import requests
from document_models import ValidationIssue


def moderate_vendor_text(text: str) -> bool:
    """Run Perspective API toxicity check on vendor notes.

    Returns True if text passes moderation (score < 0.5).\n"""
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {
        "key": os.getenv("PERSPECTIVE_API_KEY"),
        "content-type": "application/json",
    }
    resp = requests.post(url, json=payload, headers=headers)
    result = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    if result >= 0.5:
        issues = [
            ValidationIssue(
                field="vendor_notes", reason=f"High toxicity score {result}"
            )
        ]
        raise ValueError(issues)
    return True
