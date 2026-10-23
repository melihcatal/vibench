import boto3
from typing import Dict, Any


def runbook_translate(text: str, source_language: str, target_language: str, config: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("translate", region_name=config.get("region"))

    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    translated_text = response["TranslatedText"]
    source_language_detected = response["SourceLanguageCode"]
    target_language_used = response["TargetLanguageCode"]

    return {
        "original_text": text,
        "translated_text": translated_text,
        "source_language_detected": source_language_detected,
        "target_language_used": target_language_used
    }
