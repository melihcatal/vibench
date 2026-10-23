from __future__ import annotations

from openai import OpenAI

from observability_client import ObservabilityConfig
from observability_models import TranslationResult


def dashboard_note_translate(text: str, source_language: str, target_language: str) -> TranslationResult:
    cfg = ObservabilityConfig()
    client = OpenAI()
    response = client.chat.completions.create(
        model=cfg.llm_model_id,
        messages=[
            {"role": "system", "content": "Translate dashboard notes accurately and briefly."},
            {"role": "user", "content": f"Translate from {source_language} to {target_language}: {text}"},
        ],
    )
    translated = response.choices[0].message.content or text
    return TranslationResult(source_text=text, translated_text=translated, source_language=source_language, target_language=target_language)
