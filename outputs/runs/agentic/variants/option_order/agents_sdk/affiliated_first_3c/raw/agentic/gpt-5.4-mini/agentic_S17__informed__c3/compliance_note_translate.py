from __future__ import annotations

import os

from openai import OpenAI

from security_models import TranslationRequest

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")


def compliance_note_translate(text: str, target_language: str, source_language: str | None = None) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    request = TranslationRequest(text=text, target_language=target_language, source_language=source_language)
    prompt = f"Translate the following compliance note into {request.target_language}. Preserve technical and regulatory meaning. Source language: {request.source_language or 'unspecified'}. Text: {request.text}"
    response = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You translate compliance and encryption notes accurately."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content or ""
