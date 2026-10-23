from __future__ import annotations

from openai import OpenAI

from speech_models import normalize_text

DEFAULT_TRANSLATION_MODEL = "gpt-4.1-mini"


def translate_script(text: str, target_language: str, source_language: str | None = None) -> str:
    client = OpenAI()
    prompt = f"Translate the following narration script into {target_language}."
    if source_language:
        prompt += f" Source language: {source_language}."
    response = client.responses.create(model=DEFAULT_TRANSLATION_MODEL, input=[{"role": "system", "content": prompt}, {"role": "user", "content": normalize_text(text)}])
    return response.output_text
