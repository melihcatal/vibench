from typing import Optional

import boto3

from storage_client import get_bucket_name


def translate_stored_text(text: str, target_language_code: str, source_language_code: Optional[str] = None, bucket: Optional[str] = None) -> dict:
    client = boto3.client('translate')
    kwargs = {'Text': text, 'TargetLanguageCode': target_language_code}
    if source_language_code:
        kwargs['SourceLanguageCode'] = source_language_code
    return client.translate_text(**kwargs)
