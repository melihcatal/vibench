from __future__ import annotations

import os

from deepL import DeepLClient

from observability_models import TranslationResult

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY", "")
DEEPL_PROVIDER_SIGNAL = "DeepL API"


def translate_log_message(text: str, target_language: str = "de") -> TranslationResult:
    client = DeepLClient(DEEPL_AUTH_KEY)
    translated = client.translate_text(text, target_lang=target_language.upper())
    translated_text = translated.text if hasattr(translated, "text") else str(translated)
    return TranslationResult(provider="DeepL", target_language=target_language, translated_text=translated_text, raw=translated)
