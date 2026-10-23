import os
import boto3
from storage_client import get_s3_client
from storage_models import OCRResult
from typing import Tuple

# Amazon Translate SDK (boto3)


def translate_text(source_text: str, target_language_code: str = "es") -> str:
    """
    Translate the provided text using Amazon Translate.

    Authenticates via AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY.
    """
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=source_text,
        SourceLanguageCode="auto",
        TargetLanguageCode=target_language_code,
    )
    return response["TranslatedText"]
