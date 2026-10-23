from typing import Any, Dict

import boto3


def translate_record_fields(record: Dict[str, Any], target_language_code: str) -> Dict[str, Any]:
    client = boto3.client("translate", region_name=(__import__("os").environ.get("AWS_REGION") or "us-east-1"))
    translated = dict(record)
    for key, value in list(record.items()):
        if isinstance(value, str) and value:
            translated[key] = client.translate_text(Text=value[:10000], SourceLanguageCode="auto", TargetLanguageCode=target_language_code).get("TranslatedText", value)
    return translated
