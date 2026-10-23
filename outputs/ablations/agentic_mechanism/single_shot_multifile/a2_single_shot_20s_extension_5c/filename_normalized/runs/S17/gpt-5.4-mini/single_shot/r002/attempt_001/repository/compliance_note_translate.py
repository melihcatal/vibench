from __future__ import annotations

import os
from typing import Any, Dict, Optional

from openai import OpenAI

from security_models import normalize_text

TRANSLATION_MODEL = "gpt-4o-mini"


def compliance_note_translate(note: Any, target_language: str = "en", api_key: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    source_text = normalize_text(note)
    prompt = f"Translate the following encryption or compliance note into {target_language} while preserving technical meaning:\n\n{source_text}"
    response = client.responses.create(model=TRANSLATION_MODEL, input=prompt)
    translated = getattr(response, "output_text", None)
    if translated is None:
        translated = ""
    return {"model": TRANSLATION_MODEL, "target_language": target_language, "source_text": source_text, "translated_text": translated}
