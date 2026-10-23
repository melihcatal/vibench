import os
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError
from model_models import PlatformResponse


def translate_platform_output(
    response: PlatformResponse, target_locale: str = "es"
) -> Dict[str, Any]:
    """Translate platform model output for another locale using AWS Translate."""
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not found in environment variables")

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        translate_response = translate_client.translate_text(
            Text=response.content[:5000],
            SourceLanguageCode="auto",
            TargetLanguageCode=target_locale,
        )

        return {
            "provider": "aws_translate",
            "original_text": response.content[:100],
            "translated_text": translate_response["TranslatedText"],
            "source_language": translate_response["SourceLanguageCode"],
            "target_language": target_locale,
            "original_model": response.model_id,
            "translation_service": "Amazon Translate",
        }

    except ClientError as e:
        return {
            "provider": "aws_translate",
            "original_model": response.model_id,
            "translation_status": "failed",
            "error_code": e.response["Error"]["Code"],
            "error_message": e.response["Error"]["Message"],
        }
