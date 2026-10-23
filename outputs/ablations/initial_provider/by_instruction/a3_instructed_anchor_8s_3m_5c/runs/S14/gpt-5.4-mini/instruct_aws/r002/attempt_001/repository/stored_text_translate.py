import boto3

from storage_client import default_bucket, s3_client
from storage_models import normalize_key, response_payload


def stored_text_translate(bucket=None, key=None, target_language_code="en"):
    bucket_name = default_bucket(bucket)
    object_key = normalize_key(key)
    body = s3_client().get_object(Bucket=bucket_name, Key=object_key)["Body"].read().decode("utf-8")
    client = boto3.client("translate")
    result = client.translate_text(Text=body, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return response_payload(provider="aws", service="translate", bucket=bucket_name, key=object_key, translated_text=result.get("TranslatedText"), source_language_code=result.get("SourceLanguageCode"), target_language_code=result.get("TargetLanguageCode"))
