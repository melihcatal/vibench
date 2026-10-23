"""
dashboard_note_translate.py
Translate metric or dashboard notes for another locale using the OpenAI Translation model.
Provider: OpenAI (api.openai.com)
"""

import os
from typing import List, Optional, Dict, Any

import openai

from observability_models import MetricAnnotation


def translate_dashboard_note(
    note_text: str,
    target_locale: str,
    model: str = "gpt-4o-mini",
    source_locale: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Translate a metric dashboard note to another locale using the OpenAI API.

    Uses the gpt-4o-mini model for fast, high-quality translations of
    dashboard annotations and metric descriptions.

    Args:
        note_text: The dashboard note or annotation text to translate.
        target_locale: Target locale code, e.g. "ja", "de", "fr", "zh".
        model: OpenAI model to use for translation (default gpt-4o-mini).
        source_locale: Optional source locale code.
        api_key: Optional OpenAI API key (falls back to OPENAI_API_KEY env var).

    Returns:
        Translated text string.
    """
    api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")

    client = openai.OpenAI(api_key=api_key)

    source_hint = f" from {source_locale}" if source_locale else ""

    system_prompt = (
        "You are a professional translator specializing in technical "
        "dashboard and monitoring terminology. Translate the given text "
        f"{source_hint} to {target_locale}. "
        "Preserve all metric names, variable placeholders, and technical "
        "terms exactly as they appear. Only output the translated text."
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": note_text},
            ],
            temperature=0.1,
            max_tokens=1024,
        )

        translated = response.choices[0].message.content.strip()
        return translated

    except openai.APIError as exc:
        raise RuntimeError(
            f"OpenAI translation failed for dashboard note: {exc}"
        ) from exc


def batch_translate_notes(
    notes: List[str],
    target_locale: str,
    model: str = "gpt-4o-mini",
    source_locale: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[str]:
    """
    Translate multiple dashboard notes to another locale via OpenAI.

    Args:
        notes: List of note texts to translate.
        target_locale: Target locale code.
        model: OpenAI model for translation.
        source_locale: Optional source locale.
        api_key: Optional OpenAI API key.

    Returns:
        List of translated strings.
    """
    results = []
    for note in notes:
        translated = translate_dashboard_note(
            note_text=note,
            target_locale=target_locale,
            model=model,
            source_locale=source_locale,
            api_key=api_key,
        )
        results.append(translated)
    return results


def translate_metric_annotation(
    annotation: MetricAnnotation,
    target_locale: str,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
) -> MetricAnnotation:
    """
    Translate a MetricAnnotation object to another locale using OpenAI.

    Args:
        annotation: The MetricAnnotation to translate.
        target_locale: Target locale code.
        model: OpenAI model for translation.
        api_key: Optional OpenAI API key.

    Returns:
        A new MetricAnnotation with translated text and locale set.
    """
    translated_text = translate_dashboard_note(
        note_text=annotation.text,
        target_locale=target_locale,
        model=model,
        api_key=api_key,
    )

    return MetricAnnotation(
        text=translated_text,
        timestamp=annotation.timestamp,
        author=annotation.author,
        tags=annotation.tags,
        safety_checked=annotation.safety_checked,
        translation_locale=target_locale,
    )


def get_available_translation_locales() -> List[str]:
    """Return common locale codes supported by OpenAI translation models."""
    return [
        "en", "es", "fr", "de", "ja", "zh", "ko", "pt", "ru",
        "it", "nl", "ar", "hi", "tr", "pl", "sv", "da", "no",
        "fi", "cs", "hu", "ro", "th", "vi", "id", "ms",
    ]
