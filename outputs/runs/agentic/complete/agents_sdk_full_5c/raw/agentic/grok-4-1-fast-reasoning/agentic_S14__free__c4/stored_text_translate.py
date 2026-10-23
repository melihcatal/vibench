import boto3
from google.cloud import translate_v2 as translate
from storage_client import get_aws_creds
from storage_models import download_object_as_text

def stored_text_translate(bucket: str, key: str, target_language: str = 'en') -> str:
    s3 = boto3.client('s3', **get_aws_creds())
    text = download_object_as_text(s3, bucket, key)
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']