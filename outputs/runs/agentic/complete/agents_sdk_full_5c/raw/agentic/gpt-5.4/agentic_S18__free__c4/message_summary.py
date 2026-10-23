from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI


OPENAI_MODEL = "gpt-4o-mini"


def summarize_message_result(processing_record: Dict[str, Any]) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize a pub/sub message processing result in one concise sentence.",
            },
            {
                "role": "user",
                "content": str(processing_record),
            },
        ],
    )
    return response.output_text.strip()
