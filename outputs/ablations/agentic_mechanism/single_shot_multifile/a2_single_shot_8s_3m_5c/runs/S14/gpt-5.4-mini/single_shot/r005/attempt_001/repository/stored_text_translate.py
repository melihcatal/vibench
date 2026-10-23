from storage_client import get_s3_client, resolve_bucket_name
from storage_models import ObjectMetadataRequest
from boto3 import client as boto3_client


def stored_text_translate(request: ObjectMetadataRequest, target_language: str) -> str:
    s3 = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    obj = s3.get_object(Bucket=bucket, Key=request.key)
    text = obj['Body'].read().decode('utf-8', errors='ignore')
    translate = boto3_client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return result.get('TranslatedText', '')
