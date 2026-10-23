from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from database_models import canonical_json


def summarize_record(record: dict[str, Any]) -> dict[str, str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Summarize a NoSQL document record in concise operational language.",
            },
            {"role": "user", "content": canonical_json(record)},
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": response.choices[0].message.content or "",
    }
