import os
import boto3
from typing import Dict, Any

def record_translate(
    record: Dict[str, Any],
    text_field: str,
    target_language: str,
    source_language: str = "auto"
) -> str:
    """
    Translates a text field from a document record using AWS Translate.

    Args:
        record: The document record.
        text_field: The key of the text field to translate.
        target_language: The ISO 639-1 code for the target language.
        source_language: The ISO 639-1 code for the source language. Defaults to "auto".

    Returns:
        The translated text.
    """
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    translate_client = boto3.client(service_name='translate', region_name=aws_region)

    text_to_translate = record.get(text_field)
    if not text_to_translate:
        return ""

    response = translate_client.translate_text(
        Text=text_to_translate,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    return response.get('TranslatedText', '')
