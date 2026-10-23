import boto3
import os

def translate_text(payload, config=None):
    config = config or {}
    region = config.get("region", "us-east-1")
    client = boto3.client("translate", region_name=region)

    text_to_translate = payload.get("text", "")
    source_language_code = payload.get("source_language", "auto") # e.g., 'en', 'es', 'auto'
    target_language_code = payload.get("target_language", "es") # e.g., 'en', 'es'

    response = client.translate_text(
        Text=text_to_translate,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )

    translated_text = response["TranslatedText"]
    return {"translated_text": translated_text}
