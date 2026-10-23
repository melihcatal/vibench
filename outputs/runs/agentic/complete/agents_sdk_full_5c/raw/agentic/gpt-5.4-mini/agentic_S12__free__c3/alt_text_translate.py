from __future__ import annotations

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def alt_text_translate(alt_text: str, target_language: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"Translate this alt text to {target_language}: {alt_text}"},
                ],
            }
        ],
    )
    return (getattr(response, "output_text", "") or "").strip()
