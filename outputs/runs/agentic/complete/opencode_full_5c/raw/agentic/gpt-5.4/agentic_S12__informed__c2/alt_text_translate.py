from __future__ import annotations

from vision_client import translate_client
from vision_models import TranslationResult


def alt_text_translate(
    text: str, target_language: str, source_language: str = "auto"
) -> dict:
    client = translate_client()
    request = {
        "Text": text,
        "TargetLanguageCode": target_language,
    }
    if source_language != "auto":
        request["SourceLanguageCode"] = source_language
    response = client.translate_text(**request)
    result = TranslationResult(
        provider="amazon-translate",
        translated_text=response.get("TranslatedText", ""),
        target_language=target_language,
        raw_response=response,
    )
    return result.to_dict()
