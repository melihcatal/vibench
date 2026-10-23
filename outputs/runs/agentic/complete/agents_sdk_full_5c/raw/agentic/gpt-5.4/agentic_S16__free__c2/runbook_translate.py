from __future__ import annotations

from security_client import get_translate_client
from security_models import TranslationResult


AWS_TRANSLATE_SOURCE = "auto"


def translate_runbook(note: str, target_language: str = "es") -> TranslationResult:
    client = get_translate_client()
    response = client.translate_text(
        Text=note,
        SourceLanguageCode=AWS_TRANSLATE_SOURCE,
        TargetLanguageCode=target_language,
    )
    return TranslationResult(
        source_text=note,
        translated_text=response["TranslatedText"],
        target_language=response["TargetLanguageCode"],
        provider="aws-translate",
    )
