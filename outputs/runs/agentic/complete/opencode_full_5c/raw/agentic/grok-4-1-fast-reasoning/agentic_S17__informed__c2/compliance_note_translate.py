import boto3
import os
from typing import Optional


def translate_compliance_note(
    note: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    client = boto3.client("translate", region_name="us-east-1")
    result = client.translate_text(
        Text=note, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return result["TranslatedText"]
