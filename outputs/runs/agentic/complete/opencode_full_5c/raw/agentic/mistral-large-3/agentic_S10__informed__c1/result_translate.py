import boto3
from typing import Dict, Any


def translate_text(
    text: str, target_language: str = "es", source_language: str = "en"
) -> str:
    """
    Translate generated model output using Amazon Translate.
    """
    client = boto3.client("translate")

    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )

    return response["TranslatedText"]
