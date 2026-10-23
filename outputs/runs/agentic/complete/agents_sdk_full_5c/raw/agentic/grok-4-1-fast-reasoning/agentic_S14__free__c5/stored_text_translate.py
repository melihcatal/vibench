import os
import boto3
from storage_client import get_s3_client, download_object
from typing import Optional

def stored_text_translate(
    bucket: str,
    key: str,
    source_language_code: str = 'en',
    target_language_code: str = 'es',
    region: Optional[str] = 'us-east-1'
) -> str:
    s3_client = get_s3_client(region)
    text_bytes = download_object(s3_client, bucket, key)
    text = text_bytes.decode('utf-8')
    translate_client = boto3.client(
        'translate',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=region
    )
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response['TranslatedText']
