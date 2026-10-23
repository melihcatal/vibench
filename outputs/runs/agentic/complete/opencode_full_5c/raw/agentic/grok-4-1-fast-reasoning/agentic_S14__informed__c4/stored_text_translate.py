import boto3
from typing import Dict
from storage_client import get_aws_client_kwargs


def stored_text_translate(
    bucket: str,
    object_key: str,
    target_language_code: str,
    source_language_code: str = "en",
) -> Dict[str, str]:
    kwargs = get_aws_client_kwargs()
    s3_client = boto3.client("s3", **kwargs)
    response = s3_client.get_object(Bucket=bucket, Key=object_key)
    text = response["Body"].read().decode("utf-8")
    translate_client = boto3.client("translate", **kwargs)
    translate_response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )
    return {
        "source_text": text,
        "translated_text": translate_response["TranslatedText"],
        "detected_source_language": translate_response["SourceLanguageCode"],
        "target_language": target_language_code,
    }
