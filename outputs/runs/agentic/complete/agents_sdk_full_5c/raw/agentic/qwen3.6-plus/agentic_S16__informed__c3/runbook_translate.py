"""
runbook_translate.py - Translate secret-rotation runbook notes using DeepL API.

Provider: DeepL API
SDK: deepl
Auth env var: DEEPL_AUTH_KEY
"""

import os
import logging
from typing import Optional, List, Dict, Any

import deepl

logger = logging.getLogger(__name__)

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def _get_deepl_client() -> deepl.Translator:
    """Create a DeepL translator client using the configured API key."""
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    return deepl.Translator(DEEPL_AUTH_KEY)


def translate_runbook_note(
    text: str,
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
) -> str:
    """
    Translate a single runbook note using DeepL.

    Args:
        text: The runbook text to translate.
        target_lang: Target language code (e.g. 'EN-US', 'DE', 'JA', 'ZH').
        source_lang: Source language code. If None, DeepL auto-detects.

    Returns:
        Translated text string.

    Raises:
        ValueError: If the text is empty or API key is missing.
        deepl.exceptions.DeepLException: On DeepL API errors.
    """
    if not text or not text.strip():
        raise ValueError("Runbook text cannot be empty")

    translator = _get_deepl_client()
    kwargs: Dict[str, Any] = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, **kwargs)
    translated = result.text
    logger.info(
        "Translated runbook note to %s via DeepL (detected source: %s)",
        target_lang,
        result.detected_source_lang if hasattr(result, "detected_source_lang") else "unknown",
    )
    return translated


def translate_runbook_notes_batch(
    texts: List[str],
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
) -> List[str]:
    """
    Translate multiple runbook notes in a single batch request via DeepL.

    Args:
        texts: List of runbook note strings to translate.
        target_lang: Target language code.
        source_lang: Source language code (auto-detected if None).

    Returns:
        List of translated strings, preserving input order.
    """
    if not texts:
        return []

    translator = _get_deepl_client()
    kwargs: Dict[str, Any] = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    results = translator.translate_text(texts, **kwargs)
    return [r.text for r in results]


def translate_rotation_runbook(
    runbook_sections: Dict[str, str],
    target_lang: str = "EN-US",
) -> Dict[str, str]:
    """
    Translate a structured secret-rotation runbook (dict of section_name -> content).

    Args:
        runbook_sections: Dict mapping section names to their text content.
        target_lang: Target language code.

    Returns:
        Dict with the same keys, values translated to the target language.
    """
    if not runbook_sections:
        return {}

    sections = list(runbook_sections.keys())
    texts = list(runbook_sections.values())

    translated_texts = translate_runbook_notes_batch(texts, target_lang)
    return dict(zip(sections, translated_texts))


def get_deepl_usage() -> Optional[Dict[str, Any]]:
    """
    Retrieve DeepL API usage statistics.

    Returns a dict with character counts and limits, or None on error.
    """
    try:
        translator = _get_deepl_client()
        usage = translator.get_usage()
        return {
            "character_count": usage.character.count,
            "character_limit": usage.character.limit,
            "document_count": getattr(usage.document, "count", 0),
            "document_limit": getattr(usage.document, "limit", 0),
            "team_document_count": getattr(usage.team_document, "count", 0),
            "team_document_limit": getattr(usage.team_document, "limit", 0),
        }
    except Exception as exc:
        logger.warning("Failed to retrieve DeepL usage: %s", exc)
        return None
