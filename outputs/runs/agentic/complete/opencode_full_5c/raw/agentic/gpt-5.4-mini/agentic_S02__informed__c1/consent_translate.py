import os

import boto3


def consent_translate(text: str, target_language: str) -> str:
    client = boto3.client("translate")
    response = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return response.get("TranslatedText", "")
