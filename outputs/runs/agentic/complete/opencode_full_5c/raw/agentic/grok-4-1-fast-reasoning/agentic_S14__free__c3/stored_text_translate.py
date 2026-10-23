import boto3
from storage_client import get_s3_client


def stored_text_translate(
    bucket: str, key: str, target_language_code: str, source_language_code: str = "auto"
) -> str:
    s3_client = get_s3_client()
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8")
    translate_client = boto3.client("translate")
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )
    return result["TranslatedText"]
