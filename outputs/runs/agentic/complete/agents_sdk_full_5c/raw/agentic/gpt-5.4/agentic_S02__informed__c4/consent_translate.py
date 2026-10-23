from __future__ import annotations

import os

import deepl

from identity_models import TranslationResult



def translate_consent_copy(text: str, target_language: str) -> TranslationResult:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language.upper())
    detected = getattr(result, "detected_source_lang", None)
    return TranslationResult(
        provider="DeepL API",
        translated_text=result.text,
        detected_source_language=detected,
        target_language=target_language.upper(),
        raw={
            "billed_characters": getattr(result, "billed_characters", None),
            "detected_source_lang": detected,
            "target_lang": target_language.upper(),
        },
    )
