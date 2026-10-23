from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI


def summarize_record(
    record: dict[str, Any], focus_fields: list[str] | None = None
) -> dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    payload = (
        record
        if not focus_fields
        else {field: record.get(field) for field in focus_fields}
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize the provided NoSQL document as concise operational bullets.",
            },
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
    }
