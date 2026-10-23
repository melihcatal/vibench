from __future__ import annotations

import os
from typing import Any

import requests

from database_models import coerce_text_fields


def check_record_text_safety(
    record: dict[str, Any], field_names: list[str]
) -> dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    text_fields = coerce_text_fields(record, field_names)
    analyses: dict[str, Any] = {}
    for field_name, text in text_fields.items():
        response = requests.post(
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            params={"key": api_key},
            json={
                "comment": {"text": text},
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
        analyses[field_name] = response.json().get("attributeScores", {})
    return {
        "provider": "perspective-api",
        "fields": analyses,
    }
