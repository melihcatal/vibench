import os
import boto3
from typing import Dict, Any

def alt_text_translate(text: str, source_language: str = 'en', target_language: str = 'es') -> Dict[str, str]:
    """
    Translates generated image descriptions using AWS Translate.

    Args:
        text: The text description to translate.
        source_language: The source language code (e.g., 'en' for English).
        target_language: The target language code (e.g., 'es' for Spanish).

    Returns:
        A dictionary containing the translated text.
    """
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    return {"translated_text": response.get('TranslatedText')}
