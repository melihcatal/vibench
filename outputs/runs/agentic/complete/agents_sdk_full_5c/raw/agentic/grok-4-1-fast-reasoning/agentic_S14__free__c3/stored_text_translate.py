from storage_client import get_s3_client
from google.cloud import translate_v2 as translate

def translate_stored_text(bucket: str, key: str, target_language: str = 'en') -> str:
    """
    Translates text from a stored text document using Google Cloud Translate.
    """
    s3 = get_s3_client()
    response = s3.get_object(Bucket=bucket, Key=key)
    text = response['Body'].read().decode('utf-8')
    
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    
    return result['translatedText']