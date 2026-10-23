import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError


def stored_text_translate(
    text: str, source_language: str = "auto", target_language: str = "en"
) -> str:
    """
    Translates text extracted from a stored document using Amazon Translate.

    Args:
        text: Text content to translate.
        source_language: Source language code (default: auto-detect).
        target_language: Target language code (default: en).

    Returns:
        str: Translated text.
    """
    translate = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        return response["TranslatedText"]
    except ClientError as e:
        raise Exception(f"Failed to translate text using Amazon Translate: {e}")
