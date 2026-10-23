from __future__ import annotations

import os
from typing import Iterable, Mapping

import requests

from database_models import extract_text_fields


def check_record_text_safety(
    record: Mapping[str, object], field_names: Iterable[str] | None = None
):
    texts = extract_text_fields(record, field_names)
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": "omni-moderation-latest",
            "input": [{"type": "text", "text": value} for value in texts.values()],
        },
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    return {"fields": list(texts.keys()), "moderation": result}
