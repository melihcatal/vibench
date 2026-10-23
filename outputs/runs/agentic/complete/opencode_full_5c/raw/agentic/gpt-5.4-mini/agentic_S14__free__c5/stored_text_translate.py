import os

import boto3

from storage_client import bucket_name, client


def stored_text_translate(
    bucket: str | None, key: str, source_language: str, target_language: str
):
    s3 = client()
    translate = boto3.client(
        "translate",
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )
    text = (
        s3.get_object(Bucket=bucket_name(bucket), Key=key)["Body"]
        .read()
        .decode("utf-8")
    )
    return translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
