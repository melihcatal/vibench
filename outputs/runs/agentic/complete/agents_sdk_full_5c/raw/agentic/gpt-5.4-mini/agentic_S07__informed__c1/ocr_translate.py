from __future__ import annotations

import os
from typing import Optional

import boto3

AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def translate_ocr_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    client = boto3.client("translate", region_name=AWS_REGION)
    kwargs = {"Text": text, "SourceLanguageCode": source_language or "auto", "TargetLanguageCode": target_language}
    response = client.translate_text(**kwargs)
    return response.get("TranslatedText", "")
