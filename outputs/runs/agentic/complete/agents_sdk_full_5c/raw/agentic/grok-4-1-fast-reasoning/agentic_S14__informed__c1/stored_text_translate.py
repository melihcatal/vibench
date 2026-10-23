import boto3
from storage_client import get_s3_client
from typing import Optional

def stored_text_translate(
    bucket: str,
    object_key: str,
    target_language_code: str,
    source_language_code: Optional[str] = None
) -> str:
    """
    Translate text extracted from a stored document using Amazon Translate.
    Assumes UTF-8 text object.
    """
    s3_client = get_s3_client()
    response = s3_client.get_object(Bucket=bucket, Key=object_key)
    text = response['Body'].read().decode('utf-8')
    
    translate_client = boto3.client('translate')
    kwargs = {
        'Text': text,
        'TargetLanguageCode': target_language_code
    }
    if source_language_code:
        kwargs['SourceLanguageCode'] = source_language_code
    result = translate_client.translate_text(**kwargs)
    return result['TranslatedText']