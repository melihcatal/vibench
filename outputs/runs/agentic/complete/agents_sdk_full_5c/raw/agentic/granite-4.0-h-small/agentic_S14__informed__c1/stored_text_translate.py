import boto3
from typing import Dict, List

from .storage_client import get_s3_client

s3 = get_s3_client()

def stored_text_translate(source_text: str, target_lang: str = 'es') -> Dict[str, str]:
    """Translate extracted text using Amazon Translate."""
    try:
        translate = boto3.client('translate')
        response = translate.translate_text(
            Text=source_text,
            SourceLanguageCode='auto',
            TargetLanguageCode=target_lang
        )
        translated = response['TranslatedText']
        return {'source': source_text, 'target': translated}
    except Exception as e:
        raise RuntimeError(f'Translation error: {e}')
