"""
[LATER-STEP] appeal_translate.py - Translate appeal text for review
using DeepL API.

Provider: DeepL
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import Optional

import deepl


DEEPL_DEFAULT_TARGET_LANG = "EN"


def translate_appeal(
    appeal_text: str,
    target_lang: str = DEEPL_DEFAULT_TARGET_LANG,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> dict:
    """
    Translate an appeal text to the target language using DeepL API.

    Args:
        appeal_text: The original appeal text to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'ES', 'FR').
        source_lang: Optional source language code. If None, DeepL auto-detects.
        auth_key: Optional DeepL auth key override.

    Returns:
        Dict with 'translated_text', 'source_lang', 'target_lang'.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(key)

    translate_kwargs = {
        "target_lang": target_lang,
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    result = translator.translate_text(appeal_text, **translate_kwargs)

    return {
        "original_text": appeal_text,
        "translated_text": result.text,
        "source_lang": result.detected_source_lang or source_lang or "auto",
        "target_lang": target_lang,
    }


def translate_appeals_batch(
    appeals: list[str],
    target_lang: str = DEEPL_DEFAULT_TARGET_LANG,
    auth_key: Optional[str] = None,
) -> list[dict]:
    """
    Translate multiple appeal texts in a batch using DeepL API.

    Args:
        appeals: List of appeal text strings to translate.
        target_lang: Target language code.
        auth_key: Optional DeepL auth key override.

    Returns:
        List of translation result dicts.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(key)

    results = translator.translate_text(appeals, target_lang=target_lang)

    translations = []
    for original, translated in zip(appeals, results):
        translations.append({
            "original_text": original,
            "translated_text": translated.text,
            "source_lang": translated.detected_source_lang or "auto",
            "target_lang": target_lang,
        })

    return translations


if __name__ == "__main__":
    sample_appeal = "I believe my content was incorrectly flagged and request a review."
    result = translate_appeal(sample_appeal, target_lang="DE")
    print(result)
