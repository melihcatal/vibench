import os
from typing import Dict
from boto3 import client
from botocore.exceptions import ClientError


def translate_text_from_stored_document(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
) -> Dict[str, str]:
    """
    Translates text extracted from a stored document using Amazon Translate.

    Args:
        text: Text to translate.
        source_language: Source language code (e.g., "auto" for auto-detection).
        target_language: Target language code (e.g., "en" for English).

    Returns:
        Dictionary containing translated text and detected source language.

    Raises:
        ClientError: If the translation fails.
    """
    translate_client = client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        return {
            "translated_text": response.get("TranslatedText"),
            "source_language": response.get("SourceLanguageCode"),
        }
    except ClientError as e:
        raise Exception(f"Failed to translate text: {e}")
