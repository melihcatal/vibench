from __future__ import annotations

from typing import Optional

from security_client import get_translate_client
from security_models import TranslationResponse


def translate_compliance_note(text: str, target_language: str, source_language: Optional[str] = "auto") -> TranslationResponse:
    translate = get_translate_client()
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language or "auto",
        TargetLanguageCode=target_language,
    )
    return TranslationResponse(
        provider="amazon-translate",
        translated_text=response["TranslatedText"],
        target_language=target_language,
        source_language=response.get("SourceLanguageCode"),
    )
