from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


def dashboard_note_translate(text: str, target_language: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Translate the following metric dashboard note into {target_language}. Preserve metric names, units, and timestamps. Return only the translated text.\n\n{text}"
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    translated = response.choices[0].message.content or ""
    return {"source": text, "target_language": target_language, "translated": translated, "model": OPENAI_MODEL}
