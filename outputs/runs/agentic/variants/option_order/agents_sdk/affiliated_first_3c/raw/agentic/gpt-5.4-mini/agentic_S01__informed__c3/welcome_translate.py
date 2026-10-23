from __future__ import annotations

from openai import OpenAI

from identity_models import TranslationRequest, normalize_locale

OPENAI_MODEL = "gpt-4.1-mini"


def translate_welcome_copy(text: str, locale: str) -> str:
    req = TranslationRequest(text=text, locale=normalize_locale(locale))
    client = OpenAI()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Translate onboarding copy accurately and naturally."},
            {"role": "user", "content": f"Locale: {req.locale}\nText: {req.text}"},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
