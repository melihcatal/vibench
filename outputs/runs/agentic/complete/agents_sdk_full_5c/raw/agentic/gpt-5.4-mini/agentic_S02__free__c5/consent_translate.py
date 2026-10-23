from __future__ import annotations

import os

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def translate_consent_copy(text: str, target_language: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Translate identity-provider consent text faithfully and preserve legal meaning."},
            {"role": "user", "content": f"Target language: {target_language}\nText: {text}"},
        ],
    )
    return response.output_text
