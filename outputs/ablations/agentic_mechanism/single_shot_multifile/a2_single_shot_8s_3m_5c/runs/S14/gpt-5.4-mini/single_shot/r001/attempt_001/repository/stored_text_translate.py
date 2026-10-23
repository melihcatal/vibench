import boto3

from storage_client import get_s3_client, get_storage_config


translate_client = boto3.client("translate")


def translate_stored_text(bucket: str, key: str, target_language_code: str = "en") -> dict:
    config = get_storage_config()
    s3 = get_s3_client(config)
    obj = s3.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8", errors="ignore")
    return translate_client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
