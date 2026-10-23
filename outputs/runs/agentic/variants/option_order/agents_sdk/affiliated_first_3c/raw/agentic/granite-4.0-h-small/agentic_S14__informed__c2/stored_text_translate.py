"""Translate extracted text using Amazon Translate.

Prerequisites:
  * AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY set in the environment for boto3.
  * Source language code (e.g., 'en') and target language code (e.g., 'es').
"""

import os

import boto3

client = boto3.client('translate')

def translate_text(source_text: str, source_lang: str, target_lang: str) -> str:
    """Translate text using Amazon Translate.

    Args:
        source_text (str): Text to translate.
        source_lang (str): ISO 639-1 source language code (e.g., 'en').
        target_lang (str): ISO 639-1 target language code (e.g., 'es').
    Returns:
        str: Translated text.
    """
    print(f"Translating [{source_lang}] -> [{target_lang}]: {source_text[:40]}...")
    response = client.translate_text(
        Text=source_text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
    )
    translated = response['TranslatedText']
    return translated

if __name__ == '__main__':
    # Example usage – expects env vars for S3 content and language codes
    INPUT_TEXT = os.getenv('INPUT_TEXT') or 'Hello, world!'
    SOURCE_LANG = os.getenv('SRC_LANG') or 'en'
    TARGET_LANG = os.getenv('TRG_LANG') or 'es'
    print('Translated:', translate_text(INPUT_TEXT, SOURCE_LANG, TARGET_LANG))
