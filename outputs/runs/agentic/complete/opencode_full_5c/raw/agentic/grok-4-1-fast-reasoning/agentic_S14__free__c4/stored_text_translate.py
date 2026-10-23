import boto3
from storage_client import get_s3_client


def translate_stored_text(
    bucket: str, key: str, source_language: str = "en", target_language: str = "es"
) -> str:
    s3_client = get_s3_client()
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8")
    translate_client = boto3.client("translate", region_name="us-east-1")
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return result["TranslatedText"]
