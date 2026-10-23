import boto3
import os
from typing import Dict

def compliance_note_translate(note: str, target_language_code: str = 'es') -> str:
    """
    Translates encryption or compliance notes using Amazon Translate.
    """
    client = boto3.client('translate')
    response = client.translate_text(
        Text=note,
        SourceLanguageCode='auto',
        TargetLanguageCode=target_language_code
    )
    return response['TranslatedText']