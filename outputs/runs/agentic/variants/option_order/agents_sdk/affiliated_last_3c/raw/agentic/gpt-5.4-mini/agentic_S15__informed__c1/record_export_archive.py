from __future__ import annotations

from typing import Optional

import boto3

from database_models import ArchiveRequest

S3_CLIENT = boto3.client("s3")


def archive_snapshot(bucket: str, object_name: str, payload: bytes, content_type: str = "application/octet-stream") -> str:
    request = ArchiveRequest(bucket=bucket, object_name=object_name, payload=payload, content_type=content_type)
    S3_CLIENT.put_object(Bucket=request.bucket, Key=request.object_name, Body=request.payload, ContentType=request.content_type)
    return f"s3://{request.bucket}/{request.object_name}"
