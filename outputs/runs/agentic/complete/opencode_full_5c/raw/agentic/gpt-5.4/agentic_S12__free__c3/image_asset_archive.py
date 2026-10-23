from __future__ import annotations

import json
import os

import boto3

from vision_models import ArchiveResult


def image_asset_archive(asset_name: str, artifacts: dict) -> ArchiveResult:
    bucket = os.environ["S3_ARCHIVE_BUCKET"]
    region = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    client = boto3.client("s3", region_name=region)
    object_key = f"image-analysis/{asset_name}.json"
    body = json.dumps(artifacts, ensure_ascii=False).encode("utf-8")
    client.put_object(
        Bucket=bucket, Key=object_key, Body=body, ContentType="application/json"
    )
    return ArchiveResult(
        provider="amazon_s3",
        bucket=bucket,
        object_key=object_key,
        uri=f"s3://{bucket}/{object_key}",
    )
