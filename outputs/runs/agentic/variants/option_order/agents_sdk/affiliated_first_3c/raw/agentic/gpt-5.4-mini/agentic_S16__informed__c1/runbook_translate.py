from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from security_models import join_lines


def translate_runbook_notes(notes: List[str], target_language: str = "es") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = join_lines(notes)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate secret-rotation runbook notes to {target_language}."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
