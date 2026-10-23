import boto3
import os

def translate_text(text: str, source_language_code: str, target_language_code: str):
    """
    Translates text using Amazon Translate.
    """
    translate_client = boto3.client('translate')
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_text = response['TranslatedText']
        print(f"Original text: '{text}'\nTranslated text ({target_language_code}): '{translated_text}'")
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

