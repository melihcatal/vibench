from __future__ import annotations

from security_client import openai_client
from security_models import TranslationResult


def compliance_note_translate(text: str, target_language: str) -> TranslationResult:
    client = openai_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate encryption or compliance review notes to {target_language}. Return only the translated text.",
            },
            {"role": "user", "content": text},
        ],
    )
    return TranslationResult(
        translated_text=response.output_text.strip(),
        target_language=target_language,
    )
