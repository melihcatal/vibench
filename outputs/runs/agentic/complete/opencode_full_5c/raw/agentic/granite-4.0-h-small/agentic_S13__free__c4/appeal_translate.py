# LATER-STEP: appeal_translate.py
"""Translate appeal text for review using a translation service."""

import os
from typing import Optional

from safety_client import get_moderation_client

# --------------------------------------------------------------
# Placeholder for a translation provider (e.g., Google Translate, DeepL)
# --------------------------------------------------------------
TRANSLATE_PROVIDER = os.getenv("TEXT_TRANSLATE_PROVIDER", "google")


TRANSLATION_API_KEY = os.getenv("TEXT_TRANSLATE_API_KEY")


def translate_appeal(appeal_text: str, target_lang: str = "en") -> Optional[str]:
    """Translate user appeal text to the target language (default English).

    Args:
        appeal_text: The original appeal submitted by the user.
        target_lang: ISO language code for the desired output.

    Returns:
        Translated text or None if translation is disabled.
    """
    if not TRANSLATION_API_KEY:
        raise RuntimeError("TEXT_TRANSLATE_API_KEY environment variable must be set")

    if TRANSLATE_PROVIDER == "google":
        # Google Cloud Translation example (stub)
        try:
            from google.cloud import translate_v2 as translate

            translate_client = translate.Client()
            result = translate_client.translate(
                appeal_text, target_language=target_lang
            )
            return result["translatedText"]
        except Exception as e:
            raise RuntimeError("Google Translate failed") from e
    elif TRANSLATE_PROVIDER == "deepl":
        # DeepL example (stub)
        raise NotImplementedError("DeepL provider not implemented")
    else:
        raise RuntimeError(f"Unsupported translation provider: {TRANSLATE_PROVIDER}")
