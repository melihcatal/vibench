import os
from pathlib import Path
from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def archive_metric_snapshot(snapshot_path: str, bucket_name: str = None, object_key: str = None) -> str:
    bucket_name = bucket_name or os.environ.get("AWS_S3_BUCKET")
    if not bucket_name:
        raise ValueError("AWS_S3_BUCKET is required")

    path = Path(snapshot_path)
    if not path.is_file():
        raise FileNotFoundError(snapshot_path)

    s3 = boto3.client("s3")
    if object_key is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        object_key = f"metrics-archive/{stamp}/{path.name}"

    try:
        s3.upload_file(str(path), bucket_name, object_key)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Failed to archive snapshot to s3://{bucket_name}/{object_key}") from exc

    return f"s3://{bucket_name}/{object_key}"
