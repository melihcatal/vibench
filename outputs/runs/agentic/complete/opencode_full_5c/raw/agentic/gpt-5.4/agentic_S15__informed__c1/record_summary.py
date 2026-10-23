from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI


def summarize_record(record: dict[str, Any]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize the provided document record in a concise factual paragraph.",
            },
            {"role": "user", "content": json.dumps(record, ensure_ascii=False)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
