import os
import boto3
from document_client import get_aws_translate_client

def translate_invoice_note(note_text: str, target_language_code: str = 'en') -> str:
    translate_client = get_aws_translate_client()

    if not note_text.strip():
        return ""

    response = translate_client.translate_text(
        Text=note_text,
        SourceLanguageCode='auto',  # Automatically detect the source language
        TargetLanguageCode=target_language_code
    )

    translated_text = response.get('TranslatedText', '')
    return translated_text
