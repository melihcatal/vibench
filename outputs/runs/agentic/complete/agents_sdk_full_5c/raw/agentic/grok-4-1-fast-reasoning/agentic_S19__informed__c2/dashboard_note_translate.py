import os
import boto3
from typing import Optional

def dashboard_note_translate(note_text: str, target_locale: str, source_locale: Optional[str] = None) -> str:
    client = boto3.client(
        'translate',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
    params = {
        'Text': note_text,
        'TargetLanguageCode': target_locale
    }
    if source_locale:
        params['SourceLanguageCode'] = source_locale
    result = client.translate_text(**params)
    return result['TranslatedText']
