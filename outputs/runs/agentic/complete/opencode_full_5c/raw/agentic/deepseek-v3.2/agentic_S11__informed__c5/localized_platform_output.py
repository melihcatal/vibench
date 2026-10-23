import os
import boto3
from typing import Optional
from dataclasses import dataclass


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    raw_response: Optional[Dict] = None


def localize_platform_output(
    text: str,
    target_language_code: str = "es",
    source_language_code: Optional[str] = None,
) -> TranslationResult:
    """
    Translate platform model output for another locale using Amazon Translate.
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    try:
        translate_client = boto3.client(
            "translate",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region,
        )

        translate_args = {
            "Text": text,
            "SourceLanguageCode": source_language_code or "auto",
            "TargetLanguageCode": target_language_code,
        }

        response = translate_client.translate_text(**translate_args)

        return TranslationResult(
            translated_text=response["TranslatedText"],
            source_language=response["SourceLanguageCode"],
            target_language=response["TargetLanguageCode"],
            raw_response=response,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to translate with Amazon Translate: {e}")
