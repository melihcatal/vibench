import os

import boto3


def invoice_note_translate(text: str, target_language: str = "es") -> str:
    client = boto3.client("translate")
    result = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return result.get("TranslatedText", "")
