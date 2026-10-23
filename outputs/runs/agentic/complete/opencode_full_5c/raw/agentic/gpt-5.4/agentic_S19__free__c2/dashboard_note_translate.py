from __future__ import annotations

import os

from openai import OpenAI


def dashboard_note_translate(text: str, target_locale: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate dashboard and metric notes into {target_locale}. Preserve technical metric names, IDs, and units exactly.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
