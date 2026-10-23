from __future__ import annotations

import os
from typing import Any, Dict

import boto3


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
TARGET_LANGUAGE_CODE = os.getenv("TARGET_LANGUAGE_CODE", "es")


def record_translate(record: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("translate", region_name=AWS_REGION)
    translated: Dict[str, Any] = dict(record)
    for key, value in list(record.items()):
        if isinstance(value, str) and value.strip():
            translated[key] = client.translate_text(Text=value, SourceLanguageCode="auto", TargetLanguageCode=TARGET_LANGUAGE_CODE)["TranslatedText"]
    return translated
