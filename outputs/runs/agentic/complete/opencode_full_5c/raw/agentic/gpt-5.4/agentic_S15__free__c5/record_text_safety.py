from __future__ import annotations

import os

from openai import OpenAI

from database_models import extract_user_text_fields


def record_text_safety(document: dict[str, object]) -> dict[str, object]:
    fields = extract_user_text_fields(document)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.moderations.create(
        model="omni-moderation-latest", input=list(fields.values())
    )
    flagged = any(result.flagged for result in response.results)
    return {
        "flagged": flagged,
        "fields": list(fields.keys()),
        "results": [result.categories.model_dump() for result in response.results],
    }
