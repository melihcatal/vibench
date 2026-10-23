from __future__ import annotations

import os

from openai import OpenAI

from model_models import TranslationResult


def translate_result(text: str, target_language: str = "en") -> TranslationResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model=os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini"),
        messages=[
            {"role": "system", "content": "You are a precise translation engine."},
            {"role": "user", "content": f"Translate to {target_language}:\n\n{text}"},
        ],
        temperature=0,
        max_tokens=1000,
    )
    translated = completion.choices[0].message.content.strip()
    return TranslationResult(source_text=text, translated_text=translated, target_language=target_language, raw=completion)
