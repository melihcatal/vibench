from __future__ import annotations

from security_client import DEFAULT_OPENAI_TRANSLATION_MODEL, get_openai_client
from security_models import TranslationResult


def compliance_note_translate(note: str, target_language: str) -> TranslationResult:
    client = get_openai_client()
    response = client.responses.create(
        model=DEFAULT_OPENAI_TRANSLATION_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Translate security, encryption, and compliance review notes accurately and preserve technical meaning.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Target language: {target_language}\n\nNote:\n{note}",
                    }
                ],
            },
        ],
    )
    return TranslationResult(
        provider="openai",
        model=DEFAULT_OPENAI_TRANSLATION_MODEL,
        translated_text=response.output_text,
    )
