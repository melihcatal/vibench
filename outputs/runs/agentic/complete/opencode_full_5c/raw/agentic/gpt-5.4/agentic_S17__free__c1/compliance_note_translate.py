from __future__ import annotations

from typing import Any, Dict, Optional

from security_client import get_translate_client
from security_models import TranslationResult


def compliance_note_translate(
    text: str,
    target_language: str,
    source_language: str = "auto",
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    translate_client = get_translate_client(region_name)
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    result = TranslationResult(
        provider="aws-translate",
        source_language=response.get("SourceLanguageCode", source_language),
        target_language=response["TargetLanguageCode"],
        translated_text=response["TranslatedText"],
    )
    return result.to_dict()
