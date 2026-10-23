from __future__ import annotations

from openai import OpenAI

from security_models import TranslationRequest

MODEL_ID = "gpt-4o-mini"


def translate_runbook(note: str, target_language: str, source_language: str = "en") -> str:
    client = OpenAI()
    request = TranslationRequest(text=note, source_language=source_language, target_language=target_language)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Translate runbook notes accurately and preserve procedural meaning."},
            {"role": "user", "content": f"Translate from {request.source_language} to {request.target_language}: {request.text}"},
        ],
    )
    return response.choices[0].message.content or ""
