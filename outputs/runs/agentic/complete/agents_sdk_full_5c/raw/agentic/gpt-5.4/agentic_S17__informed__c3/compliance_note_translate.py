from __future__ import annotations

import deepl

from security_client import get_required_env
from security_models import TranslationResult, normalize_text_payload



def compliance_note_translate(note: str, target_language: str) -> TranslationResult:
    auth_key = get_required_env("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(normalize_text_payload(note), target_lang=target_language)
    return TranslationResult(
        provider="deepl",
        target_language=target_language,
        translated_text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
    )
