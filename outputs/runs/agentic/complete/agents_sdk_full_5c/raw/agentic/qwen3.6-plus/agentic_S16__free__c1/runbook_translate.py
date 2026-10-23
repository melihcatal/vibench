"""
runbook_translate.py - Translate secret-rotation runbook notes using DeepL API.

Uses the DeepL translation API (api-free.deepl.com) to translate runbook
notes and rotation procedures between languages for global teams.
"""

from __future__ import annotations

import logging
import os
from typing import Optional, List, Dict, Any

import deepl

from security_models import TranslationResult

logger = logging.getLogger(__name__)

DEEPL_API_HOST = "api-free.deepl.com"


def get_deepl_client() -> deepl.Translator:
    """Create a DeepL translator client using the DEEPL_API_KEY environment variable."""
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")
    return deepl.Translator(api_key)


def translate_runbook_note(
    source_text: str,
    target_language: str = "EN-US",
    source_language: str = "auto",
) -> TranslationResult:
    """
    Translate a secret-rotation runbook note using the DeepL API.

    Args:
        source_text: The runbook note text to translate.
        target_language: Target language code (e.g., EN-US, DE, JA, FR).
        source_language: Source language code or 'auto' for auto-detection.

    Returns:
        TranslationResult with the translated text and metadata.
    """
    translator = get_deepl_client()
    logger.info(
        "Translating runbook note via DeepL (%s -> %s): %d chars",
        source_language,
        target_language,
        len(source_text),
    )

    try:
        result = translator.translate_text(
            source_text,
            source_lang=source_language if source_language != "auto" else None,
            target_lang=target_language,
        )

        translation = TranslationResult(
            source_text=source_text,
            translated_text=result.text,
            source_language=result.detected_source_lang if hasattr(result, "detected_source_lang") else source_language,
            target_language=target_language,
            provider="deepl",
        )

        logger.info(
            "Translation complete: %d -> %d chars",
            len(source_text),
            len(translation.translated_text),
        )
        return translation

    except deepl.DeepLException as e:
        logger.error("DeepL translation failed: %s", e)
        raise


def translate_runbook_batch(
    notes: List[str],
    target_language: str = "EN-US",
    source_language: str = "auto",
) -> List[TranslationResult]:
    """
    Translate a batch of runbook notes using the DeepL API.

    Args:
        notes: List of runbook note strings to translate.
        target_language: Target language code.
        source_language: Source language code or 'auto'.

    Returns:
        List of TranslationResult objects.
    """
    translator = get_deepl_client()
    logger.info("Translating batch of %d notes via DeepL to %s", len(notes), target_language)

    try:
        results = translator.translate_text(
            notes,
            source_lang=source_language if source_language != "auto" else None,
            target_lang=target_language,
        )

        translations = []
        for i, result in enumerate(results):
            translations.append(
                TranslationResult(
                    source_text=notes[i],
                    translated_text=result.text,
                    source_language=result.detected_source_lang if hasattr(result, "detected_source_lang") else source_language,
                    target_language=target_language,
                    provider="deepl",
                )
            )

        logger.info("Batch translation complete: %d notes translated", len(translations))
        return translations

    except deepl.DeepLException as e:
        logger.error("DeepL batch translation failed: %s", e)
        raise


def get_supported_languages() -> List[Dict[str, Any]]:
    """
    Get list of supported languages from the DeepL API.

    Returns:
        List of dicts with language code and name.
    """
    translator = get_deepl_client()
    target_langs = translator.get_target_languages()
    return [{"code": lang.code, "name": lang.name} for lang in target_langs]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    runbook_text = (
        "Secret rotation procedure: 1) Trigger rotation via AWS Console. "
        "2) Verify AWSPENDING stage is populated. 3) Test new credentials. "
        "4) Promote AWSPENDING to AWSCURRENT. 5) Validate application connectivity."
    )
    result = translate_runbook_note(runbook_text, target_language="DE")
    print(f"Source ({result.source_language}): {result.source_text}")
    print(f"Target ({result.target_language}): {result.translated_text}")
    print(f"Provider: {result.provider}")
