from __future__ import annotations

from storage_client import create_translate_client
from storage_models import TranslationResult



def translate_extracted_text(text: str, target_language: str, source_language: str = "auto") -> TranslationResult:
    client = create_translate_client()
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    metadata = response.get("ResponseMetadata", {})
    return TranslationResult(
        source_text=text,
        translated_text=response["TranslatedText"],
        source_language=response.get("SourceLanguageCode"),
        target_language=response["TargetLanguageCode"],
        provider_request_id=metadata.get("RequestId"),
    )
