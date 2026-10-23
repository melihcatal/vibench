from storage_client import s3_config
import boto3


def translate_stored_document_text(
    bucket: str, key: str, source_language: str = "en", target_language: str = "es"
) -> str:
    s3_client = boto3.client("s3", **s3_config)
    resp = s3_client.get_object(Bucket=bucket, Key=key)
    text = resp["Body"].read().decode("utf-8")
    translate_client = boto3.client("translate", **s3_config)
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return result["TranslatedText"]
