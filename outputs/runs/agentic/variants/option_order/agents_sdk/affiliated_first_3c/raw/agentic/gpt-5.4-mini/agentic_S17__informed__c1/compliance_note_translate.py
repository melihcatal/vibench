from __future__ import annotations

import json

from openai import OpenAI

PROVIDER = "OpenAI Chat Completions"
TRANSLATION_MODEL = "gpt-4o-mini"


def compliance_note_translate(text: str, target_language: str = "es") -> str:
    client = OpenAI()
    prompt = f"Translate the following encryption or compliance note into {target_language} while preserving meaning and terminology:\n\n{text}"
    response = client.chat.completions.create(model=TRANSLATION_MODEL, messages=[{"role": "user", "content": prompt}])
    translated = response.choices[0].message.content or ""
    return json.dumps({"provider": PROVIDER, "model": TRANSLATION_MODEL, "translated_text": translated})
