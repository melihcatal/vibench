from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

PROVIDER_NAME = "OpenAI"
MODEL_ID = "gpt-4o-mini"


def translate_record_fields(fields: Dict[str, str], target_language: str, source_language: str | None = None) -> Dict[str, str]:
    client = OpenAI()
    translated: Dict[str, str] = {}
    for key, value in fields.items():
        prompt = f"Translate the following text to {target_language}. Return only the translation. Source language: {source_language or 'unspecified'}. Text: {value}"
        response = client.chat.completions.create(model=MODEL_ID, messages=[{"role": "user", "content": prompt}])
        translated[key] = response.choices[0].message.content or ""
    return translated
