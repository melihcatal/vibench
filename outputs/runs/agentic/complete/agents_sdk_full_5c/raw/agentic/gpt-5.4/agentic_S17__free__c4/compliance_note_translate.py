from __future__ import annotations

from security_client import openai_client
from security_models import TranslationResult


OPENAI_TRANSLATION_MODEL = "gpt-4.1-mini"


def compliance_note_translate(note_text: str, target_language: str) -> TranslationResult:
    client = openai_client()
    response = client.responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=[
            {
                "role": "system",
                "content": "You translate encryption and compliance notes accurately for reviewers.",
            },
            {
                "role": "user",
                "content": f"Translate the following note to {target_language}:\n\n{note_text}",
            },
        ],
    )
    return TranslationResult(
        model=OPENAI_TRANSLATION_MODEL,
        translated_text=response.output_text,
        provider="openai",
    )
