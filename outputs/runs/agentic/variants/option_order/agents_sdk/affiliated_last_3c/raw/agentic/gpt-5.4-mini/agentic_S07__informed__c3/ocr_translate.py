from __future__ import annotations

from typing import Optional

import boto3

from document_models import normalize_text


def translate_ocr_text(text: str, target_language_code: str, source_language_code: Optional[str] = None, region_name: Optional[str] = None) -> str:
    client = boto3.client("translate", region_name=region_name)
    response = client.translate_text(
        Text=normalize_text(text),
        SourceLanguageCode=source_language_code or "auto",
        TargetLanguageCode=target_language_code,
    )
    return response.get("TranslatedText", "")
