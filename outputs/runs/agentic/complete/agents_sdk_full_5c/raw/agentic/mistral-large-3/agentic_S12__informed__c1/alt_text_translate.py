import os
from typing import Dict
import boto3
from vision_models import ImageDescriptionResponse


def translate_alt_text(description: ImageDescriptionResponse, target_language: str) -> str:
    """Translate generated image descriptions using Amazon Translate."""
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1"
    )

    response = translate_client.translate_text(
        Text=description.description,
        SourceLanguageCode="auto",
        TargetLanguageCode=target_language
    )

    return response.get("TranslatedText", "")