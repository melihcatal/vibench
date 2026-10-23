import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError


def appeal_translate(
    appeal_text: str, target_language: str = "en", source_language: Optional[str] = None
) -> str:
    """
    Translate appeal text for review using Amazon Translate.
    """
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
        if source_language:
            response = translate_client.translate_text(
                Text=appeal_text,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )
        else:
            response = translate_client.translate_text(
                Text=appeal_text, TargetLanguageCode=target_language
            )

        return response["TranslatedText"]

    except ClientError as e:
        raise Exception(f"Translation failed: {e}")
