import boto3
import os
from typing import Dict, Any

def translate_compliance_note(note: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    region = os.getenv('AWS_REGION', 'us-east-1')
    translate_client = boto3.client('translate', region_name=region)
    response = translate_client.translate_text(
        Text=note,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )
    return response['TranslatedText']
