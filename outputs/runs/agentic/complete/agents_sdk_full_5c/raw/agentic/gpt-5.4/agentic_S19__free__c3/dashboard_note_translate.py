from __future__ import annotations

from openai import OpenAI


OPENAI_MODEL = "gpt-4o-mini"


def dashboard_note_translate(note: str, target_locale: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": f"Translate monitoring dashboard notes into {target_locale}. Preserve metric names, resource IDs, and numeric values.",
            },
            {"role": "user", "content": note},
        ],
    )
    return response.output_text
