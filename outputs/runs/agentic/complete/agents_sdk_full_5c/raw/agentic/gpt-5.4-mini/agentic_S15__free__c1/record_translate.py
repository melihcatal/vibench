from typing import Any, Dict, Iterable

import boto3


def translate_record(record: Dict[str, Any], target_language: str = "es", fields: Iterable[str] = ("title", "content", "body")) -> Dict[str, Any]:
    client = boto3.client("translate")
    translated = dict(record)
    for field in fields:
        value = record.get(field)
        if isinstance(value, str) and value:
            translated[field] = client.translate_text(Text=value, SourceLanguageCode="auto", TargetLanguageCode=target_language).get("TranslatedText", value)
    return translated
