from __future__ import annotations

from typing import Any, Dict

import boto3

from model_client import load_config



def localized_platform_output(text: str) -> Dict[str, Any]:
    config = load_config()
    client = boto3.client("translate", region_name=config.aws_region)
    result = client.translate_text(
        Text=text,
        SourceLanguageCode="en",
        TargetLanguageCode=config.translation_target_locale,
    )
    return {
        "provider": "Amazon Translate",
        "translated_text": result["TranslatedText"],
        "source_language": result.get("SourceLanguageCode", "en"),
        "target_language": result.get("TargetLanguageCode", config.translation_target_locale),
    }
