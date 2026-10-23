import boto3
from typing import Optional

def stored_text_translate(
    text: str,
    target_language: str = 'es'
) -> str:
    translate_client = boto3.client('translate')
    result = translate_client.translate_text(
        Text=text,
        TargetLanguageCode=target_language
    )
    return result['TranslatedText']