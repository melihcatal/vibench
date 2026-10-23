"""
Translate appeal text for review using cloud translation service.
Provider: DeepL API (deepl SDK).
Auth: DEEPL_AUTH_KEY
"""

import os
import json
from typing import Optional, List, Dict

import deepl


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def translate_appeal(
    appeal_text: str,
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> Dict:
    """
    Translate an appeal text for moderation review using DeepL API.

    Args:
        appeal_text: The original appeal text to translate.
        target_lang: Target language code (e.g., 'EN-US', 'DE', 'FR', 'JA', 'ZH').
        source_lang: Optional source language code. If None, DeepL auto-detects.
        auth_key: Optional DeepL auth key override.

    Returns:
        Dictionary with original text, translated text, source/target languages, and provider info.
    """
    key = auth_key or DEEPL_AUTH_KEY
    if not key:
        raise ValueError("DEEPL_AUTH_KEY is required for DeepL API access.")

    translator = deepl.Translator(key)

    translate_kwargs = {"target_lang": target_lang}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    result = translator.translate_text(appeal_text, **translate_kwargs)

    return {
        "original_text": appeal_text,
        "translated_text": result.text,
        "source_lang": result.detected_source_lang if hasattr(result, "detected_source_lang") else source_lang or "auto",
        "target_lang": target_lang,
        "provider": "DeepL API",
    }


def translate_appeal_batch(
    appeal_texts: List[str],
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> Dict:
    """
    Translate a batch of appeal texts for moderation review using DeepL API.

    Args:
        appeal_texts: List of appeal texts to translate.
        target_lang: Target language code.
        source_lang: Optional source language code for auto-detection override.
        auth_key: Optional DeepL auth key override.

    Returns:
        Dictionary with batch translation results.
    """
    key = auth_key or DEEPL_AUTH_KEY
    if not key:
        raise ValueError("DEEPL_AUTH_KEY is required for DeepL API access.")

    translator = deepl.Translator(key)

    translate_kwargs = {"target_lang": target_lang}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    translations = []
    for text in appeal_texts:
        result = translator.translate_text(text, **translate_kwargs)
        translations.append({
            "original_text": text,
            "translated_text": result.text,
            "source_lang": result.detected_source_lang if hasattr(result, "detected_source_lang") else source_lang or "auto",
        })

    return {
        "translations": translations,
        "total_count": len(appeal_texts),
        "target_lang": target_lang,
        "provider": "DeepL API",
    }


if __name__ == "__main__":
    sample = "Mein Konto wurde zu Unrecht gesperrt. Ich bitte um Überprüfung."
    result = translate_appeal(sample, target_lang="EN-US")
    print(json.dumps(result, indent=2))
