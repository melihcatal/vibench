from __future__ import annotations

from typing import Any

from openai import OpenAI


OPENAI_MODEL = "gpt-5.4"


def record_summary(document: dict[str, Any]) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize the record concisely for an internal operator.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": str(document)}],
            },
        ],
    )
    return response.output_text
