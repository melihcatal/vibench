from __future__ import annotations

from openai import OpenAI


def log_message_translate(message: str, locale: str = "es") -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate support-visible log messages into {locale}. Preserve identifiers and technical terms."},
            {"role": "user", "content": message},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""
