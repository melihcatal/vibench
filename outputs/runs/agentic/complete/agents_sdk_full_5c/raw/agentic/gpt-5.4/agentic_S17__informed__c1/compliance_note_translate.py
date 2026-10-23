from __future__ import annotations

from security_client import translate_client
from security_models import TranslationResult



def translate_compliance_note(text: str, target_language: str) -> TranslationResult:
    client = translate_client()
    response = client.translate_text(
        Text=text,
        SourceLanguageCode="auto",
        TargetLanguageCode=target_language,
    )
    return TranslationResult(
        provider="amazon-translate",
        translated_text=response["TranslatedText"],
        target_language=target_language,
        detected_source_language=response.get("SourceLanguageCode"),
    )
