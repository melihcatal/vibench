from __future__ import annotations

import os

from openai import OpenAI


def log_message_translate(message: str, target_locale: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate support-visible log messages into {target_locale} while preserving technical identifiers.",
            },
            {"role": "user", "content": message},
        ],
    )
    return response.output_text
