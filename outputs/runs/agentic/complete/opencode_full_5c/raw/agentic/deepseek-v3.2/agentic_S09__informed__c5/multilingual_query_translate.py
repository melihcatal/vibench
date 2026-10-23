import os
import boto3
from typing import Optional


def translate_query(
    query: str, target_language: str = "en", source_language: Optional[str] = None
) -> str:
    """Translate queries before multilingual embedding search using Amazon Translate."""
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "us-east-1")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    try:
        response = translate_client.translate_text(
            Text=query,
            SourceLanguageCode=source_language or "auto",
            TargetLanguageCode=target_language,
        )

        return response["TranslatedText"]

    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")
