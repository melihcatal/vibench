import boto3

from storage_client import get_default_bucket, get_s3_client
from storage_models import normalize_key


def stored_text_translate(
    bucket: str, key: str, source_language: str, target_language: str
):
    s3 = get_s3_client()
    translate = boto3.client("translate")
    obj = s3.get_object(Bucket=bucket, Key=normalize_key(key))
    text = obj["Body"].read().decode("utf-8")
    return translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )


def stored_text_translate_default(key: str, source_language: str, target_language: str):
    return stored_text_translate(
        get_default_bucket(), key, source_language, target_language
    )
