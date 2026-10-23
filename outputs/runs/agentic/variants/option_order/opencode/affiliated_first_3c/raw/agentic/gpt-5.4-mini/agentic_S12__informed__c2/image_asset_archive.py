import os
import boto3


def image_asset_archive(bucket: str, key: str, body: bytes) -> dict:
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=key, Body=body)
    return {
        "bucket": bucket,
        "key": key,
        "version": os.environ.get("AWS_SESSION_TOKEN", ""),
    }


__all__ = ["image_asset_archive"]
