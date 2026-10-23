from __future__ import annotations

import os

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def welcome_translate(copy: str, locale: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "system",
                "content": "Translate onboarding copy for product emails while preserving meaning and tone.",
            },
            {"role": "user", "content": f"Locale: {locale}\n\nCopy:\n{copy}"},
        ],
    )
    return response.output_text
