import os
import boto3
from typing import Dict, Any

def translate_stored_text(
    text: str,
    source_language_code: str = 'auto',
    target_language_code: str = 'en'
) -> Dict[str, Any]:
    """
    Translates text using Amazon Translate.

    Args:
        text: The text string to translate.
        source_language_code: The language code of the input text (e.g., 'en', 'es').
                              Use 'auto' for automatic language detection.
        target_language_code: The language code to translate the text into (e.g., 'en', 'fr').

    Returns:
        A dictionary containing the translation response.
    """
    translate_client = boto3.client(
        'translate',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

    try:
        if source_language_code == 'auto':
            response = translate_client.translate_text(
                Text=text,
                TargetLanguageCode=target_language_code
            )
        else:
            response = translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code
            )
        return response
    except Exception as e:
        print(f"Error translating text with Amazon Translate: {e}")
        raise
