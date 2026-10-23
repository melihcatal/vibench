import boto3
import os

translate_client = boto3.client('translate')

def translate_text(text: str, target_language: str = 'es', source_language: str = 'en') -> str:
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return result['TranslatedText']
