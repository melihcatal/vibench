from __future__ import annotations

from openai import OpenAI


def dashboard_note_translate(text: str, target_locale: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate dashboard and metrics notes into locale {target_locale} while preserving technical terminology.",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    return response.output_text
