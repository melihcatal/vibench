import os
from typing import Dict, Any


def appeal_translate(appeal_text: str, target_language: str = "en") -> Dict[str, Any]:
    """
    Translate appeal text for review using Amazon Translate.
    """
    import boto3

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
        response = translate_client.translate_text(
            Text=appeal_text,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language,
        )

        return {
            "original_text": appeal_text,
            "translated_text": response["TranslatedText"],
            "source_language": response.get("SourceLanguageCode", "auto"),
            "target_language": target_language,
            "provider": "amazon_translate",
            "service": "aws translate",
        }

    except Exception as e:
        return {
            "original_text": appeal_text,
            "translated_text": appeal_text,
            "source_language": "unknown",
            "target_language": target_language,
            "error": str(e),
            "provider": "amazon_translate",
        }
