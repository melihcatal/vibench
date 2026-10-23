import os
from typing import Dict, Any

import boto3

def translate_dashboard_note(
    text: str,
    source_language_code: str,
    target_language_code: str
) -> Dict[str, Any]:
    translate_client = boto3.client('translate')

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )

    translated_text = response.get('TranslatedText')
    source_lang = response.get('SourceLanguageCode')
    target_lang = response.get('TargetLanguageCode')

    return {
        "original_text": text,
        "translated_text": translated_text,
        "source_language": source_lang,
        "target_language": target_lang,
    }
