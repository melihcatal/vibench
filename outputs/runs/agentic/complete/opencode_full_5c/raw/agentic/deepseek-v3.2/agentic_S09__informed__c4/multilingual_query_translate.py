import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError


def translate_query(
    query: str, target_language: str = "en", source_language: Optional[str] = None
) -> str:
    """Translate queries before multilingual embedding search using Amazon Translate."""
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        translate_args = {
            "Text": query,
            "SourceLanguageCode": source_language or "auto",
            "TargetLanguageCode": target_language,
        }

        response = translate_client.translate_text(**translate_args)
        translated_text = response["TranslatedText"]

        return translated_text

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "UnsupportedLanguagePairException":
            return query
        else:
            raise Exception(f"Amazon Translate error: {str(e)}")
