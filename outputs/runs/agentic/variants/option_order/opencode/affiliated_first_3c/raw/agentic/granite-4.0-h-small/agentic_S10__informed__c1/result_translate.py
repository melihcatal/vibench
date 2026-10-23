import os
import requests

# Environment var for translation provider (Amazon Translate)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

if not (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY):
    raise RuntimeError("AWS credentials not set")

from boto3 import client as boto3_client

translate_client = boto3_client(
    "translate",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


def translate_text(text: str, target_language: str = "es") -> str:
    """Translates text using Amazon Translate.

    Returns the translated string."""
    response = translate_client.TranslateText(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
