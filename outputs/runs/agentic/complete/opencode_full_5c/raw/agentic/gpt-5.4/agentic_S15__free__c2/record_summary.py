from __future__ import annotations

import os
from typing import Any, Dict, Iterable

from openai import OpenAI


def record_summary(documents: Iterable[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    payload = [dict(item) for item in documents]
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize document records concisely for operators.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": str(payload)}],
            },
        ],
    )
    return response.output_text
