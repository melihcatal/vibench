import boto3
import os


def save_audio(payload, config=None):
    config = config or {}
    s3_client = boto3.client("s3", region_name=config.get("region"))
    bucket_name = config.get("s3_bucket_name", os.environ.get("AWS_S3_BUCKET_NAME"))
    file_key = payload.get("file_key")
    audio_bytes = payload.get("audio_bytes")
    content_type = payload.get("content_type", "audio/mpeg")

    if not bucket_name:
        raise ValueError("S3 bucket name not provided in config or environment variables.")
    if not file_key:
        raise ValueError("File key (object name) not provided in payload.")
    if not audio_bytes:
        raise ValueError("Audio bytes not provided in payload.")

    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=audio_bytes, ContentType=content_type)

    return {"s3_uri": f"s3://{bucket_name}/{file_key}"}
