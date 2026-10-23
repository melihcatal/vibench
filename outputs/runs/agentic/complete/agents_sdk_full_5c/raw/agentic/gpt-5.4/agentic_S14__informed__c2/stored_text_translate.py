from __future__ import annotations

from storage_client import translate_client
from storage_models import TranslationResult


TRANSLATE_PROVIDER = "Amazon Translate"


def translate_extracted_text(text: str, target_language: str, source_language: str = "auto") -> TranslationResult:
    client = translate_client()
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return TranslationResult(
        source_text=text,
        translated_text=response["TranslatedText"],
        source_language=response.get("SourceLanguageCode"),
        target_language=target_language,
    )


def translate_extracted_text_dict(text: str, target_language: str, source_language: str = "auto") -> dict:
    return translate_extracted_text(text=text, target_language=target_language, source_language=source_language).to_dict()
