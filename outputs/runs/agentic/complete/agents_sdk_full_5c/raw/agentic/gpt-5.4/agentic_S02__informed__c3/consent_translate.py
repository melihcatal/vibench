from __future__ import annotations

from typing import Optional

import deepl

from identity_models import TranslationResult


class ConsentCopyTranslator:
    def __init__(self, auth_key: str, *, server_url: Optional[str] = None):
        self.translator = deepl.Translator(auth_key, server_url=server_url)

    def translate(self, text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
        result = self.translator.translate_text(
            text,
            target_lang=target_language,
            source_lang=source_language,
        )
        detected = source_language or getattr(result, "detected_source_lang", None)
        return TranslationResult(
            provider="DeepL API",
            source_language=detected,
            target_language=target_language,
            translated_text=result.text,
            raw={
                "billed_characters": getattr(result, "billed_characters", None),
                "detected_source_lang": getattr(result, "detected_source_lang", None),
            },
        )
