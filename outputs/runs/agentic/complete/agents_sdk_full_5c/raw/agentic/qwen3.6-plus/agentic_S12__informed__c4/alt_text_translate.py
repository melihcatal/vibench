"""
alt_text_translate.py - Translate generated image descriptions
using Google Cloud Translation API (google-cloud-translate SDK).

Provider: Google Cloud Translation
SDK: google-cloud-translate
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional

from google.cloud import translate_v2 as translate

from vision_models import ImageDescription


# Default target language codes for alt text translation
COMMON_TARGET_LANGUAGES = ["es", "fr", "de", "ja", "zh-CN", "pt", "ar"]


def translate_description(
    description: str,
    target_language: str = "es",
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """Translate a single image description string.

    Args:
        description: The English (or source) description text.
        target_language: BCP-47 target language code.
        source_language: Optional source language code (auto-detect if None).
        api_key: Optional API key override.

    Returns:
        Translated description string.
    """
    client = translate.Client()

    translate_params: Dict[str, str] = {
        "q": description,
        "target_language": target_language,
    }
    if source_language:
        translate_params["source_language"] = source_language

    result = client.translate(**translate_params)

    if isinstance(result, dict):
        return result.get("translatedText", description)
    return result


def translate_description_multi(
    description: str,
    target_languages: Optional[List[str]] = None,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    """Translate an image description into multiple target languages.

    Args:
        description: The source description text.
        target_languages: List of BCP-47 target language codes.
        source_language: Optional source language code.

    Returns:
        Dict mapping language code to translated text.
    """
    targets = target_languages or COMMON_TARGET_LANGUAGES
    translations: Dict[str, str] = {}

    for lang_code in targets:
        try:
            translated = translate_description(
                description=description,
                target_language=lang_code,
                source_language=source_language,
            )
            translations[lang_code] = translated
        except Exception:
            translations[lang_code] = description  # fallback

    return translations


def translate_alt_text(
    image_desc: ImageDescription,
    target_languages: Optional[List[str]] = None,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    """Translate the description from an ImageDescription into multiple languages.

    Args:
        image_desc: The ImageDescription object from describe_image.py.
        target_languages: List of target BCP-47 codes.
        source_language: Source language code for translation.

    Returns:
        Dict mapping language code to translated alt text.
    """
    return translate_description_multi(
        description=image_desc.description,
        target_languages=target_languages,
        source_language=source_language or "en",
    )


def format_translation_report(
    original: str,
    translations: Dict[str, str],
) -> str:
    """Format a human-readable translation report."""
    lines = [
        "=== Alt Text Translation Report (Google Cloud Translation) ===",
        "",
        f"Original: {original}",
        "",
        "Translations:",
    ]
    for lang_code, text in sorted(translations.items()):
        lines.append(f"  [{lang_code}] {text}")
    return "\n".join(lines)


if __name__ == "__main__":
    sample_desc = ImageDescription(
        description="A red barn in a green field at sunset.",
        confidence=0.95,
        topics=["barn", "field", "sunset", "agriculture"],
    )

    results = translate_alt_text(sample_desc)
    print(format_translation_report(sample_desc.description, results))
