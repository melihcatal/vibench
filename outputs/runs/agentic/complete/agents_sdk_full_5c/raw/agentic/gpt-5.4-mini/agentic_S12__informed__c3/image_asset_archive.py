from __future__ import annotations

import os

import boto3

from vision_models import ArchiveRecord

S3_BUCKET = os.getenv("IMAGE_ARCHIVE_BUCKET", "image-analysis-archive")
S3_PREFIX = os.getenv("IMAGE_ARCHIVE_PREFIX", "derived/")
S3_CLIENT = boto3.client("s3")


def archive_image_artifacts(image_id: str, artifacts: dict) -> ArchiveRecord:
    key = f"{S3_PREFIX}{image_id}.json"
    S3_CLIENT.put_object(Bucket=S3_BUCKET, Key=key, Body=str(artifacts).encode("utf-8"), ContentType="application/json")
    return ArchiveRecord(bucket=S3_BUCKET, key=key, uri=f"s3://{S3_BUCKET}/{key}")
