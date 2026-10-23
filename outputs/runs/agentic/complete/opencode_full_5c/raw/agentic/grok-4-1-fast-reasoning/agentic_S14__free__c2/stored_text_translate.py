import boto3
from storage_client import get_s3_client


def stored_text_translate(
    bucket: str, key: str, source_language: str = "en", target_language: str = "es"
) -> str:
    s3_client = get_s3_client()
    response = s3_client.get_object(Bucket=bucket, Key=key)
    text = response["Body"].read().decode("utf-8")
    translate_client = boto3.client("translate")
    translated = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return translated["TranslatedText"]
