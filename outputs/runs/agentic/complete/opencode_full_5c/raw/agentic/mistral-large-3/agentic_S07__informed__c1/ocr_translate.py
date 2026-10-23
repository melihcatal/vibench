import os
from typing import Dict, List
import boto3


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translates extracted OCR text using Amazon Translate.
    """
    client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    response = client.translate_text(
        Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return response.get("TranslatedText", "")
