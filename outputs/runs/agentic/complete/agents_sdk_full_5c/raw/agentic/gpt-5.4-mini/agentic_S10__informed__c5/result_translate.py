from __future__ import annotations

import os

from openai import OpenAI

from model_models import TranslationRequest

TRANSLATION_MODEL = "gpt-4o-mini"


def translate_result(text: str, target_language: str, source_language: str | None = None) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    req = TranslationRequest(text=text, target_language=target_language, source_language=source_language)
    instruction = f"Translate the following text into {req.target_language}."
    if req.source_language:
        instruction += f" The source language is {req.source_language}."
    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[{"role": "system", "content": "You are a precise translation engine."}, {"role": "user", "content": f"{instruction}\n\nText:\n{req.text}"}],
        temperature=0,
    )
    return response.choices[0].message.content or ""
