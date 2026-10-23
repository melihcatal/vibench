import json

import boto3


def translate_runbook_notes(text: str, target_language: str):
    client = boto3.client("translate")
    response = client.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language)
    return response.get("TranslatedText")
