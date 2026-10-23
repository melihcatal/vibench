from __future__ import annotations

from typing import Optional

from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_extracted_text(
    text: str,
    target_language_code: str,
    source_language_code: str = "auto",
    region_name: Optional[str] = None,
) -> TranslationResult:
    translate = get_translate_client(region_name)
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )
    metadata = response.get("ResponseMetadata", {})
    return TranslationResult(
        source_language=response.get("SourceLanguageCode"),
        target_language=response["TargetLanguageCode"],
        translated_text=response["TranslatedText"],
        provider_request_id=metadata.get("RequestId"),
    )
