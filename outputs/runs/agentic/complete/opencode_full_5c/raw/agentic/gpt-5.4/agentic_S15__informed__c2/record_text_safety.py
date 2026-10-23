from __future__ import annotations

import os
from typing import Any

import requests

from database_models import filter_user_text_fields


def check_record_text_safety(record: dict[str, Any]) -> dict[str, Any]:
    fields = filter_user_text_fields(record)
    analyses: dict[str, Any] = {}
    for field_name, text in fields.items():
        response = requests.post(
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            params={"key": os.environ["PERSPECTIVE_API_KEY"]},
            json={
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {
                    "TOXICITY": {},
                    "INSULT": {},
                    "THREAT": {},
                },
            },
            timeout=30,
        )
        response.raise_for_status()
        analyses[field_name] = response.json()
    return analyses
