import boto3
from typing import Optional
from storage_client import S3_CONFIG, BUCKET_NAME

def translate_stored_text(
    key: str,
    source_language: str = 'en',
    target_language: str = 'es'
) -> str:
    s3_client = boto3.client('s3', **S3_CONFIG)
    obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
    text = obj['Body'].read().decode('utf-8')
    
    translate_client = boto3.client('translate')
    resp = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return resp['TranslatedText']
