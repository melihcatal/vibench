import os
from datetime import datetime, timezone
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

S3_BUCKET_ENV = "AWS_S3_BUCKET"
S3_PREFIX_ENV = "AWS_S3_PREFIX"
AWS_REGION_ENV = "AWS_REGION"
AWS_PROFILE_ENV = "AWS_PROFILE"


def _s3_client():
    session = boto3.Session(profile_name=os.getenv(AWS_PROFILE_ENV) or None, region_name=os.getenv(AWS_REGION_ENV) or None)
    return session.client("s3")


def archive_exported_metric_snapshot(source_path: str, object_key: Optional[str] = None) -> str:
    bucket = os.environ[S3_BUCKET_ENV]
    prefix = os.getenv(S3_PREFIX_ENV, "metrics-archive").strip("/")
    key = object_key or f"{prefix}/{datetime.now(timezone.utc).strftime('%Y/%m/%d/%H%M%S')}-{os.path.basename(source_path)}"
    client = _s3_client()
    try:
        client.upload_file(source_path, bucket, key)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"failed to archive snapshot to s3://{bucket}/{key}") from exc
    return f"s3://{bucket}/{key}"


__all__ = ["archive_exported_metric_snapshot"]
