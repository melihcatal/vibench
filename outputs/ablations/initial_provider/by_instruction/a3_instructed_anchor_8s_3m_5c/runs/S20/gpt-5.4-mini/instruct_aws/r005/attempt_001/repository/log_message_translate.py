from __future__ import annotations

import boto3


def log_message_translate(message: str, source_lang: str = "en", target_lang: str = "es"):
    client = boto3.client("translate", region_name="us-east-1")
    response = client.translate_text(Text=message, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response.get("TranslatedText", "")
