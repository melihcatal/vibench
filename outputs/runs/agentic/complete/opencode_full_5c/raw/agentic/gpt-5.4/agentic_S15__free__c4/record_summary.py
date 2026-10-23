from __future__ import annotations

import os
from typing import Iterable, Mapping

from openai import OpenAI


def summarize_records(records: Iterable[Mapping[str, object]]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    payload = [dict(record) for record in records]
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize managed NoSQL document records concisely.",
            },
            {
                "role": "user",
                "content": str(payload),
            },
        ],
    )
    return response.output_text
