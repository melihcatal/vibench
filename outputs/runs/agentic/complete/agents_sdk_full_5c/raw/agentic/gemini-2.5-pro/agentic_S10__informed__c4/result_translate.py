import boto3
from botocore.exceptions import BotoCoreError, ClientError

def translate_text(text: str, target_language: str, source_language: str = "auto") -> str:
    """
    Translates text using Amazon Translate.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language.
        source_language: The ISO 639-1 code for the source language. Defaults to 'auto'.

    Returns:
        The translated text, or an error message if translation fails.
    """
    try:
        translate_client = boto3.client('translate')
        
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        
        return response.get('TranslatedText', '')
        
    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred with Amazon Translate: {e}")
        return f"Error: Could not translate text."
