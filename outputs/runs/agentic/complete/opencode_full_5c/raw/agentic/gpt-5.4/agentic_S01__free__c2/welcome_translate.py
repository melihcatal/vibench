from __future__ import annotations

from typing import Dict

from identity_client import get_openai_client
from identity_models import TranslationResult


OPENAI_TRANSLATION_MODEL = "gpt-4.1-mini"


def welcome_translate(text: str, locale: str) -> Dict[str, str]:
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=[
            {
                "role": "system",
                "content": "Translate onboarding copy faithfully and preserve intent.",
            },
            {"role": "user", "content": f"Locale: {locale}\nText: {text}"},
        ],
    )
    translated_text = response.output_text.strip()
    return TranslationResult(
        locale=locale, translated_text=translated_text, model=OPENAI_TRANSLATION_MODEL
    ).to_dict()
