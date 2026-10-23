import os
from typing import Optional
import boto3
from storage_client import get_storage_client

def translate_stored_text(
    object_key: str,
    target_language: str,
    output_object_key: Optional[str] = None
) -> str:
    """
    Translates text extracted from a stored document in AWS S3 using AWS Translate.
    Returns the translated text.
    """
    s3_client = get_storage_client()
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

    bucket_name = os.getenv("AWS_S3_BUCKET_NAME", "default-bucket")
    output_key = output_object_key or f"translate-output/{object_key}.txt"

    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=object_key
    )
    text = response["Body"].read().decode("utf-8")

    translate_response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode="auto",
        TargetLanguageCode=target_language
    )

    translated_text = translate_response["TranslatedText"]

    s3_client.put_object(
        Bucket=bucket_name,
        Key=output_key,
        Body=translated_text.encode("utf-8")
    )

    return translated_text