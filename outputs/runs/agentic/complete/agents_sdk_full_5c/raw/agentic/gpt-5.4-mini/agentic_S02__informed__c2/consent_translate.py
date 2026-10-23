from __future__ import annotations

from typing import Dict

import boto3

AWS_TRANSLATE_REGION = "us-east-1"


def translate_consent_copy(text: str, source_language: str, target_language: str) -> Dict[str, str]:
    client = boto3.client("translate", region_name=AWS_TRANSLATE_REGION)
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return {
        "provider": "Amazon Translate",
        "translated_text": response["TranslatedText"],
        "source_language": source_language,
        "target_language": target_language,
    }
