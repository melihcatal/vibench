from __future__ import annotations

import os

from openai import OpenAI

from speech_models import normalize_text


MODEL = os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def translate_script(script: str, target_language: str, source_language: str = "en") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Translate the following narration script from {source_language} to {target_language}. Preserve line breaks and timing cues. Return only the translated script."
    response = client.responses.create(model=MODEL, input=[{"role": "system", "content": prompt}, {"role": "user", "content": normalize_text(script)}])
    return response.output_text.strip()
