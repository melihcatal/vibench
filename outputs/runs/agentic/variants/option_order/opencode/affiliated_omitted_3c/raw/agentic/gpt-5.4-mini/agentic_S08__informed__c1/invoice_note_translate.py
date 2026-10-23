from typing import Any
import boto3


def invoice_note_translate(text: str, target_language: str = 'es') -> str:
    client = boto3.client('translate')
    response = client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response.get('TranslatedText', '')
