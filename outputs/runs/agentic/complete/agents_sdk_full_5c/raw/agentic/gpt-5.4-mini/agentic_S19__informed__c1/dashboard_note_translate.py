from __future__ import annotations

from openai import OpenAI

from observability_models import TranslationResult, normalize_text

MODEL_ID = "gpt-4o-mini"


def translate_dashboard_note(text: str, target_locale: str, source_locale: str = "en") -> TranslationResult:
    normalized = normalize_text(text)
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Translate dashboard and metric notes accurately and preserve meaning."},
            {"role": "user", "content": f"Translate from {source_locale} to {target_locale}: {normalized}"},
        ],
    )
    translated = response.choices[0].message.content or ""
    return TranslationResult(source_text=normalized, translated_text=translated, source_locale=source_locale, target_locale=target_locale, provider_result=response.model_dump() if hasattr(response, "model_dump") else response)
