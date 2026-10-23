import os

from boto3 import client as boto3_client

from vision_client import load_config


def image_asset_archive(
    artifact_name: str, content: bytes, content_type: str = "text/plain"
):
    config = load_config()
    bucket = config.storage_bucket or os.getenv("AWS_S3_BUCKET")
    s3 = boto3_client("s3")
    key = artifact_name.lstrip("/")
    s3.put_object(Bucket=bucket, Key=key, Body=content, ContentType=content_type)
    return {"bucket": bucket, "key": key, "provider": "aws_s3"}
