from __future__ import annotations

import os
from typing import Dict
from typing import Iterable

import requests

from database_models import collect_text_fields


def check_record_text_safety(
    document: Dict[str, object], fields: Iterable[str]
) -> Dict[str, object]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    text_fields = collect_text_fields(document, fields)
    joined_text = "\n".join(f"{name}: {value}" for name, value in text_fields.items())
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": joined_text},
            "languages": ["en"],
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
        key.lower(): value["summaryScore"]["value"]
        for key, value in payload.get("attributeScores", {}).items()
    }
    return {
        "provider": "Perspective API",
        "analyzed_fields": list(text_fields.keys()),
        "scores": scores,
    }
