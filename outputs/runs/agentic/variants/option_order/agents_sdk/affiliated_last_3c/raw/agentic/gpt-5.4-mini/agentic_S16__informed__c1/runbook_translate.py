from __future__ import annotations

import os
from typing import Dict

from openai import OpenAI

TRANSLATION_MODEL = "gpt-4.1-mini"


def translate_runbook_notes(text: str, target_language: str) -> Dict[str, str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": f"Translate the following secret rotation runbook into {target_language}."},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
    )
    return {"model": TRANSLATION_MODEL, "translation": completion.choices[0].message.content or ""}
