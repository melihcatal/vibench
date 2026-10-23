from __future__ import annotations

import deepl

from security_client import get_deepl_auth_key
from security_models import TranslationResponse


DEEPL_FORMALITY = "prefer_more"


def translate_compliance_note(text: str, target_language: str) -> TranslationResponse:
    translator = deepl.Translator(get_deepl_auth_key())
    result = translator.translate_text(
        text,
        target_lang=target_language,
        formality=DEEPL_FORMALITY,
    )
    return TranslationResponse(
        source_text=text,
        translated_text=result.text,
        target_language=target_language,
        provider="deepl",
    )
