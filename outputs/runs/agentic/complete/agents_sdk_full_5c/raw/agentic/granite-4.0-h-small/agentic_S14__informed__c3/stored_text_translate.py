import os
from google.cloud import translate_v2 as translate

def translate_text_from_stored(bucket_name: str, object_key: str, target_lang: str = 'es') -> str:
    """Extract text from a stored document (assumed plain text) and translate it.

    Uses Google Cloud Translation API. Credentials are read from GOOGLE_APPLICATION_CREDENTIALS.
    The document is first downloaded from S3, then translated.
    """
    from storage_client import get_s3_client
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    text = obj['Body'].read().decode('utf-8')

    client = translate.Client()
    result = client.translate(text, target_language=target_lang)
    return result['translatedText']
