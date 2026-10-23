"""
Translate metric or dashboard notes for another locale.

Provider: OpenAI Translation via chat completions (openai)
Uses openai OpenAI client and api.openai.com with gpt-4o-mini model
for translation of metric annotations and dashboard notes.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import openai

from observability_models import MetricAnnotation

# Supported locales for translation
SUPPORTED_LOCALES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese (Simplified)",
    "ko": "Korean",
    "pt": "Portuguese",
    "it": "Italian",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
}


def translate_dashboard_note(
    annotation: MetricAnnotation,
    target_locale: str,
    openai_api_key: Optional[str] = None,
    translation_model: str = "gpt-4o-mini",
) -> MetricAnnotation:
    """
    Translate a metric annotation or dashboard note to another locale using OpenAI.

    Uses the OpenAI gpt-4o-mini model via api.openai.com chat completions API
    to translate annotation title and content while preserving technical metric
    terminology and dashboard context.

    Args:
        annotation: MetricAnnotation to translate.
        target_locale: Target locale code (e.g., 'es', 'fr', 'ja').
        openai_api_key: OpenAI API key (or set OPENAI_API_KEY env var).
        translation_model: OpenAI model for translation, default gpt-4o-mini.

    Returns:
        New MetricAnnotation with translated title and content.

    Raises:
        ValueError: If target_locale is not supported.
    """
    if target_locale not in SUPPORTED_LOCALES:
        raise ValueError(
            f"Unsupported locale '{target_locale}'. "
            f"Supported: {', '.join(SUPPORTED_LOCALES.keys())}"
        )

    api_key = openai_api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OpenAI API key required. Set OPENAI_API_KEY or pass openai_api_key.")

    target_language = SUPPORTED_LOCALES[target_locale]

    system_prompt = (
        "You are a professional technical translator specializing in DevOps and "
        "observability dashboard content. Translate metric names, technical terms, "
        "and alert messages accurately while preserving formatting. Keep metric names "
        "and technical identifiers (like 'cpu_usage', 'error_rate') in their original form. "
        f"Translate all user-facing text to {target_language}."
    )

    user_prompt = (
        f"Translate the following dashboard annotation:\n\n"
        f"Title: {annotation.title}\n"
        f"Content: {annotation.content}\n\n"
        f"Provide the translation in the format:\n"
        f"Title: <translated title>\n"
        f"Content: <translated content>"
    )

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=translation_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=500,
        temperature=0.2,
    )

    translated_text = response.choices[0].message.content.strip() if response.choices else ""

    # Parse translation response
    translated_title = annotation.title
    translated_content = annotation.content

    if "Title:" in translated_text:
        parts = translated_text.split("Content:", 1)
        title_part = parts[0].replace("Title:", "").strip()
        if title_part:
            translated_title = title_part
        if len(parts) > 1:
            translated_content = parts[1].strip()
    else:
        # Fallback: treat entire response as translated content
        translated_content = translated_text

    return MetricAnnotation(
        title=translated_title,
        content=translated_content,
        tags=annotation.tags + [f"locale:{target_locale}", "translated"],
        source=f"translated-from-{annotation.source if annotation.source else 'original'}",
    )


def batch_translate_notes(
    annotations: List[MetricAnnotation],
    target_locale: str,
    openai_api_key: Optional[str] = None,
    translation_model: str = "gpt-4o-mini",
) -> List[MetricAnnotation]:
    """
    Translate multiple dashboard notes to another locale.

    Uses OpenAI gpt-4o-mini via api.openai.com for each annotation.

    Args:
        annotations: List of annotations to translate.
        target_locale: Target locale code.
        openai_api_key: OpenAI API key.
        translation_model: OpenAI model to use.

    Returns:
        List of translated MetricAnnotation objects.
    """
    translated: List[MetricAnnotation] = []
    for annotation in annotations:
        try:
            result = translate_dashboard_note(
                annotation=annotation,
                target_locale=target_locale,
                openai_api_key=openai_api_key,
                translation_model=translation_model,
            )
            translated.append(result)
        except Exception as exc:
            # Return original with error tag on failure
            error_annotation = MetricAnnotation(
                title=annotation.title,
                content=f"[Translation failed: {str(exc)}]",
                tags=annotation.tags + ["translation-error"],
                source=annotation.source,
            )
            translated.append(error_annotation)
    return translated


def get_supported_locales() -> Dict[str, str]:
    """Return dict of supported locale codes and names."""
    return dict(SUPPORTED_LOCALES)
