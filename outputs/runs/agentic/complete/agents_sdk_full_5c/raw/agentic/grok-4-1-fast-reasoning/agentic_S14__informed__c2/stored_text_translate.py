import boto3
from storage_client import get_s3_client, get_bucket_name

def stored_text_translate(
    bucket_name: str | None = None,
    key: str,
    source_language: str = "en",
    target_language: str = "es"
) -> dict:
    if bucket_name is None:
        bucket_name = get_bucket_name()
    s3_client = get_s3_client()
    obj = s3_client.get_object(Bucket=bucket_name, Key=key)
    text = obj["Body"].read().decode("utf-8")
    translate_client = boto3.client("translate")
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return {
        "translated_text": result["TranslatedText"],
        "source_language": result["SourceLanguageCode"],
        "target_language": result["TargetLanguageCode"]
    }
