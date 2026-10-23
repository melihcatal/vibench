from __future__ import annotations

import os

from openai import OpenAI


OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def log_message_translate(message: str, target_locale: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=[
            {"role": "system", "content": "Translate support-visible operational log messages accurately and preserve identifiers, timestamps, and error codes."},
            {"role": "user", "content": f"Target locale: {target_locale}\nMessage: {message}"},
        ],
    )
    return response.output_text
