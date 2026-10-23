from __future__ import annotations

import boto3


def compliance_note_translate(text: str, target_language: str = "es", region_name: str | None = None) -> dict:
    client = boto3.client("translate", region_name=region_name)
    response = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language)
    return {"provider": "Amazon Translate", "translated_text": response.get("TranslatedText", ""), "source_language": response.get("SourceLanguageCode"), "target_language": target_language}
