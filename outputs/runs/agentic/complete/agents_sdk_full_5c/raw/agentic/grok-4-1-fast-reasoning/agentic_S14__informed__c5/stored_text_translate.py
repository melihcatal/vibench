import boto3
from storage_client import get_storage_client
from botocore.exceptions import ClientError
from typing import Optional

def translate_stored_document_text(bucket: str, key: str, source_language: str = 'en', target_language: str = 'es') -&gt; str:
    """
    Download text from stored document and translate using Amazon Translate.
    Assumes UTF-8 text file.
    """
    s3 = get_storage_client()
    translate = boto3.client('translate')
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        text = obj['Body'].read().decode('utf-8')
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return response['TranslatedText']
    except ClientError as e:
        raise ValueError(f"Translation failed: {e}")