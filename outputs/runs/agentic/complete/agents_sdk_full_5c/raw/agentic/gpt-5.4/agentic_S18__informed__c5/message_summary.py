from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_message_processing(result: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Summarize message processing outcomes for operations teams in 2 concise sentences.",
            },
            {
                "role": "user",
                "content": f"Create a concise audit summary for this processing result: {result}",
            },
        ],
    )
    return response.choices[0].message.content or ""
