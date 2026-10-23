from __future__ import annotations

from security_client import build_translate_client
from security_models import TranslationResult


def translate_runbook_notes(
    text: str,
    target_language: str,
    source_language: str = "auto",
    region_name: str | None = None,
) -> TranslationResult:
    client = build_translate_client(region_name)
    params = {
        "Text": text,
        "TargetLanguageCode": target_language,
    }
    if source_language and source_language != "auto":
        params["SourceLanguageCode"] = source_language
    response = client.translate_text(**params)
    detected = response.get("SourceLanguageCode") if source_language == "auto" else source_language
    return TranslationResult(
        source_language=detected,
        target_language=response["TargetLanguageCode"],
        translated_text=response["TranslatedText"],
    )
