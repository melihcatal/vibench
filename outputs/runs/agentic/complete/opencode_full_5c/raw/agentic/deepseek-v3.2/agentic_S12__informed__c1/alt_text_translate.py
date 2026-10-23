import os
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError


def alt_text_translate(description: str, target_language: str = "es") -> str:
    """
    Translate generated image descriptions using Amazon Translate.

    Args:
        description: Image description text to translate
        target_language: Target language code (default: Spanish)

    Returns:
        Translated description
    """
    client = boto3.client(
        "translate",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        response = client.translate_text(
            Text=description,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language,
        )

        return response["TranslatedText"]

    except ClientError as e:
        raise Exception(f"Amazon Translate error: {e.response['Error']['Message']}")
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")
