import boto3
import os

from translation_client import get_aws_credentials

def translate_markup(
    html_content: str, target_language: str, source_language: str = "en"
) -> str:
    """
    Translates HTML content while preserving markup, using Amazon Translate.

    Args:
        html_content: An HTML string.
        target_language: The target language code (e.g., 'de', 'ja').
        source_language: The source language code (e.g., 'en').

    Returns:
        The translated HTML string.
    """
    aws_access_key_id, aws_secret_access_key, aws_region = get_aws_credentials()

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    response = translate_client.translate_text(
        Text=html_content,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
        Settings={"Formality": "FORMAL"},
        ContentType="html",
    )

    return response.get("TranslatedText", "")
