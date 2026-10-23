from __future__ import annotations

from typing import Any, Dict, Optional

import boto3

from security_client import aws_region
from security_models import TranslationResult



def compliance_note_translate(text: str, target_language: str, source_language: Optional[str] = "auto") -> TranslationResult:
    client = boto3.client("translate", region_name=aws_region())
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language or "auto",
        TargetLanguageCode=target_language,
    )
    return TranslationResult(
        provider="amazon-translate",
        source_language=response.get("SourceLanguageCode"),
        target_language=response["TargetLanguageCode"],
        translated_text=response["TranslatedText"],
    )



def compliance_note_translate_dict(text: str, target_language: str, source_language: Optional[str] = "auto") -> Dict[str, Any]:
    result = compliance_note_translate(text=text, target_language=target_language, source_language=source_language)
    return {
        "provider": result.provider,
        "source_language": result.source_language,
        "target_language": result.target_language,
        "translated_text": result.translated_text,
    }
