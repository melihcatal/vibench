import boto3
from storage_client import get_s3_client

def translate_stored_text(bucket_name: str, object_key: str, target_language: str = 'es') -> str:
    """Translate text extracted from a stored document using AWS Translate.

    Returns translated text.
    """
    s3_client = get_s3_client()
    # Assume the object is plain text (or retrieve content first)
    obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    source_text = obj['Body'].read().decode('utf-8')
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=source_text,
        SourceLanguageCode='auto',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']