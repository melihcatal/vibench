import os
from typing import Any, Dict

import boto3

from translation_models import normalize_language_code, normalize_text


def load_translation_config(config: Dict[str, Any] = None) -> Dict[str, Any]:
    merged = dict(config or {})
    if "region" not in merged:
        merged["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return merged


def create_translation_client(config: Dict[str, Any] = None):
    loaded = load_translation_config(config)
    return boto3.client("translate", region_name=loaded.get("region"))


def translate_with_client(client, text: Any, source_language: str, target_language: str) -> Dict[str, str]:
    response = client.translate_text(
        Text=normalize_text(text),
        SourceLanguageCode=normalize_language_code(source_language),
        TargetLanguageCode=normalize_language_code(target_language),
    )
    return {
        "text": response["TranslatedText"],
        "source_language": normalize_language_code(source_language),
        "target_language": normalize_language_code(target_language),
    }
