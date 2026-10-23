import os
from typing import Optional

import boto3


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_translate_client():
    return boto3.client("translate", region_name=get_aws_region())


def translate_text_via_aws(text: str, source_language: Optional[str], target_language: str) -> str:
    client = get_translate_client()
    params = {"Text": text, "TargetLanguageCode": target_language}
    if source_language:
        params["SourceLanguageCode"] = source_language
    return client.translate_text(**params)["TranslatedText"]


def translate_text_html_via_aws(text: str, source_language: Optional[str], target_language: str) -> str:
    client = get_translate_client()
    params = {"Text": text, "TargetLanguageCode": target_language, "Settings": {"Formality": "FORMAL"}, "TerminologyNames": []}
    if source_language:
        params["SourceLanguageCode"] = source_language
    return client.translate_text(**params, ContentType="text/html")["TranslatedText"]
