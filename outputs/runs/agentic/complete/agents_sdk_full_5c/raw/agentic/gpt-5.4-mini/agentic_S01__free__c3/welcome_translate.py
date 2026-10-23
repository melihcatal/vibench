from __future__ import annotations

import os

from openai import OpenAI

MODEL = "gpt-4o-mini"


def welcome_translate(text: str, locale: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Translate onboarding copy naturally and preserve product terminology."},
            {"role": "user", "content": f"Locale: {locale}\nCopy: {text}"},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
