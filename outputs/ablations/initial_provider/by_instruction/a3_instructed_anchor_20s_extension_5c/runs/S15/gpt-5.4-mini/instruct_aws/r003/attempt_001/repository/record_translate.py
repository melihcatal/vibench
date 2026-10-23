from typing import Any, Dict

import boto3


def record_translate(record: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    translate = boto3.client("translate", region_name="us-east-1")
    translated = {}
    for key, value in record.items():
        if isinstance(value, str):
            translated[key] = translate.translate_text(Text=value[:5000], SourceLanguageCode="auto", TargetLanguageCode=target_language).get("TranslatedText")
        else:
            translated[key] = value
    return translated
