from __future__ import annotations

from openai import OpenAI


OPENAI_MODEL = "gpt-4o-mini"


def log_message_translate(message: str, target_locale: str):
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Translate support-visible operational log messages faithfully. Preserve identifiers, timestamps, codes, and stack trace fragments.",
            },
            {
                "role": "user",
                "content": f"Target locale: {target_locale}\nMessage: {message}",
            },
        ],
    )
    return {"target_locale": target_locale, "translated_text": response.output_text}
