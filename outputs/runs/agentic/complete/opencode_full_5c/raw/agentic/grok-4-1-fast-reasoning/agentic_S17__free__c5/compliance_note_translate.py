import boto3
import os
from typing import Optional


def translate_compliance_note(note: str, target_language: str = "es") -> str:
    region = os.getenv("AWS_REGION", "us-east-1")
    translate_client = boto3.client("translate", region_name=region)
    response = translate_client.translate_text(
        Text=note, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
