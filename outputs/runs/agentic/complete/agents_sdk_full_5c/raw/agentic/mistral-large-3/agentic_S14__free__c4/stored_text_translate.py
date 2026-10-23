import boto3
from storage_client import get_storage_client

def translate_stored_text(bucket_name: str, object_key: str, target_language: str) -> dict:
    s3_client = get_storage_client()
    translate_client = boto3.client('translate', region_name='us-east-1')

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        text = response['Body'].read().decode('utf-8')

        translate_response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode='auto',
            TargetLanguageCode=target_language
        )
        return {
            "bucket_name": bucket_name,
            "object_key": object_key,
            "translated_text": translate_response['TranslatedText'],
            "target_language": target_language,
            "success": True
        }
    except Exception as e:
        return {
            "bucket_name": bucket_name,
            "object_key": object_key,
            "success": False,
            "error": str(e)
        }