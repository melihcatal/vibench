from __future__ import annotations

from typing import Any, Dict, Mapping

import boto3

from database_models import extract_field_text


def record_translate(record: Mapping[str, Any], target_language: str = "es") -> Dict[str, Any]:
    client = boto3.client("translate", region_name="us-east-1")
    text = extract_field_text(record, ["title", "summary", "body", "content"])
    response = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language)
    return {"translated_text": response.get("TranslatedText", ""), "target_language": target_language}
