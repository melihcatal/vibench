from __future__ import annotations

from openai import OpenAI


def alt_text_translate(text: str, target_language: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"Translate this image alt text into {target_language}, preserving brevity: {text}",
        max_output_tokens=80,
    )
    return response.output_text.strip()
