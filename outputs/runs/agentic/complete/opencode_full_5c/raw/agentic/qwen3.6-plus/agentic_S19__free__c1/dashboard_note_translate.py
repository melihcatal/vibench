import os
from typing import Optional

import openai

from observability_models import TranslationResult


OPENAI_MODEL = "gpt-4o-mini"


def dashboard_note_translate(
    note: str,
    target_language: str,
    source_language: str = "en",
) -> TranslationResult:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        return TranslationResult(
            source_text=note,
            translated_text="",
            source_language=source_language,
            target_language=target_language,
            confidence=0.0,
        )

    language_names = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "zh": "Chinese",
        "ko": "Korean",
        "pt": "Portuguese",
        "it": "Italian",
        "ru": "Russian",
        "ar": "Arabic",
        "hi": "Hindi",
    }

    target_name = language_names.get(target_language, target_language)
    source_name = language_names.get(source_language, source_language)

    prompt = (
        f"Translate the following metric dashboard note from {source_name} to {target_name}. "
        f"Preserve any technical terms, metric names, and numbers exactly as they appear. "
        f"Do not add any extra text or explanations. Only return the translation.\n\n"
        f"Note: {note}"
    )

    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional translator specializing in technical and observability documentation.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.2,
        )
        translated = response.choices[0].message.content.strip()

        confidence = _estimate_translation_confidence(note, translated)

        return TranslationResult(
            source_text=note,
            translated_text=translated,
            source_language=source_language,
            target_language=target_language,
            confidence=confidence,
        )

    except Exception:
        return TranslationResult(
            source_text=note,
            translated_text="",
            source_language=source_language,
            target_language=target_language,
            confidence=0.0,
        )


def translate_dashboard_notes(
    notes: list[str],
    target_language: str,
    source_language: str = "en",
) -> list[TranslationResult]:
    results = []
    for note in notes:
        result = dashboard_note_translate(note, target_language, source_language)
        results.append(result)
    return results


def _estimate_translation_confidence(source: str, translated: str) -> float:
    if not translated:
        return 0.0
    source_len = len(source)
    translated_len = len(translated)
    if source_len == 0 or translated_len == 0:
        return 0.0
    ratio = min(source_len, translated_len) / max(source_len, translated_len)
    return min(0.95, ratio * 0.8 + 0.15)
