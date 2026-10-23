import os
from typing import Any

from deep_translator import GoogleTranslator

SOURCE_LANG = os.environ.get("CONSENT_SOURCE_LANG", "en")
TARGET_LANG = os.environ.get("CONSENT_TARGET_LANG", "es")


def translate_consent_copy(text: str, target_language: str | None = None) -> dict[str, Any]:
    translator = GoogleTranslator(source=SOURCE_LANG, target=target_language or TARGET_LANG)
    translated = translator.translate(text)
    return {"source_language": SOURCE_LANG, "target_language": target_language or TARGET_LANG, "translated_text": translated}
