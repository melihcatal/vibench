from __future__ import annotations

import os

from openai import OpenAI

from security_client import DEFAULT_TRANSLATION_MODEL


def translate_runbook_notes(
    notes: str, target_language: str, model: str = DEFAULT_TRANSLATION_MODEL
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": f"Translate secret rotation runbook notes into {target_language} while preserving operational meaning.",
            },
            {"role": "user", "content": notes},
        ],
    )
    return response.output_text
