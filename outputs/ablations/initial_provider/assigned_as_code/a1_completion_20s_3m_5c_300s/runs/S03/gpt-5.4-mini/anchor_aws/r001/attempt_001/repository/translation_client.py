import os
from typing import Any, Dict

import boto3


def get_translation_config(config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    merged = dict(config or {})
    merged.setdefault("region", os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    return merged


def get_translation_client(config: Dict[str, Any] | None = None):
    merged = get_translation_config(config)
    return boto3.client("translate", region_name=merged.get("region"))


def translate_with_client(client, text: str, source_language: str, target_language: str) -> str:
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
