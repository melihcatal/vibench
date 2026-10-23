import os
import boto3

def translate_markup(text: str, source_language: str, target_language: str) -> str:
    """
    Translates HTML or markup while preserving tags using AWS Translate.

    Args:
        text: The HTML or markup string to translate.
        source_language: The language of the input text (e.g., "en", "fr").
        target_language: The language to translate the text into (e.g., "es", "de").

    Returns:
        The translated HTML or markup string.
    """
    client = boto3.client("translate", region_name=os.environ.get("AWS_REGION"))

    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
        TextType='HTML'
    )
    return response['TranslatedText']
