from __future__ import annotations

import os

from openai import OpenAI


def log_message_translate(message_text: str, target_locale: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4",
        input=[
            {
                "role": "system",
                "content": "Translate support-visible log messages while preserving technical meaning.",
            },
            {
                "role": "user",
                "content": f"Translate this log message to {target_locale}: {message_text}",
            },
        ],
    )
    return response.output_text
