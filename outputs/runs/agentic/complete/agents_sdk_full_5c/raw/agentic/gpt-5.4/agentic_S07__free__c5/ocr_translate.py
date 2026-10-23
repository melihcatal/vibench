from __future__ import annotations

import os

from openai import OpenAI


MODEL = "gpt-4o-mini"
PROVIDER = "openai"


def ocr_translate(text: str, target_language: str, source_language: str | None = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    source_hint = source_language or "auto-detect"
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": "Translate OCR-extracted document text faithfully and preserve structure.",
            },
            {
                "role": "user",
                "content": f"Source language: {source_hint}\nTarget language: {target_language}\n\n{text}",
            },
        ],
    )
    return response.output_text.strip()
