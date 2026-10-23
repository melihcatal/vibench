from __future__ import annotations

from openai import OpenAI


OPENAI_MODEL = "gpt-4o-mini"


def log_message_translate(message: str, target_locale: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Translate support-visible operational log messages accurately and preserve technical fields.",
            },
            {
                "role": "user",
                "content": f"Translate this log message to {target_locale}: {message}",
            },
        ],
    )
    return response.output_text
