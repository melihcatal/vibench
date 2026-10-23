import boto3
import os
from typing import Optional

def translate_compliance_note(
    note: str,
    source_language: str = 'en',
    target_language: str = 'es'
) -> str:
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    translate_client = boto3.client('translate', region_name=region)
    resp = translate_client.translate_text(
        Text=note,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return resp['TranslatedText']