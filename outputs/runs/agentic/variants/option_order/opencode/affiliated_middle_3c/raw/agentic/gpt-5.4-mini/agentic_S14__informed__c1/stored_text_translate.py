import boto3

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_key


def translate_stored_text(key: str, target_language_code: str) -> dict:
    bucket = get_bucket_name()
    s3 = get_s3_client()
    translate = boto3.client("translate")
    normalized_key = normalize_key(key)
    body = (
        s3.get_object(Bucket=bucket, Key=normalized_key)["Body"].read().decode("utf-8")
    )
    return translate.translate_text(
        Text=body, SourceLanguageCode="auto", TargetLanguageCode=target_language_code
    )
