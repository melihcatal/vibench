from __future__ import annotations

from security_client import deepl_client
from security_models import TranslationResult



def translate_compliance_note(text: str, target_language: str = "DE") -> TranslationResult:
    client = deepl_client()
    result = client.translate_text(text, target_lang=target_language)
    return TranslationResult(
        provider="deepl",
        translated_text=result.text,
        target_language=target_language,
        detected_source_language=getattr(result, "detected_source_lang", None),
    )
