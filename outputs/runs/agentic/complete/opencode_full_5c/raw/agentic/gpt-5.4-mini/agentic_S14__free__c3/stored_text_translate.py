import os

import boto3

from storage_client import get_s3_client


def stored_text_translate(bucket: str, key: str, target_language_code: str):
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8")
    translate = boto3.client(
        "translate", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    return translate.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code
    )
