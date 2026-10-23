from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


def summarize_record(record: dict[str, Any]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize a NoSQL document record for internal operators in 2-4 sentences.",
            },
            {"role": "user", "content": str(record)},
        ],
    )
    return response.output_text
