from __future__ import annotations

import os

from openai import OpenAI


OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def log_message_translate(message: str, target_locale: str = "es") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=[
            {"role": "system", "content": f"Translate support-visible application log text into locale {target_locale}. Preserve placeholders, IDs, and technical tokens."},
            {"role": "user", "content": message},
        ],
    )
    return response.output_text
