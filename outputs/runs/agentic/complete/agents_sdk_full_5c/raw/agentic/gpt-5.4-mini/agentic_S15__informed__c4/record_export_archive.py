import os
from typing import Any, Dict

import boto3

S3_BUCKET = os.getenv("AWS_S3_EXPORT_BUCKET", "document-export-archive")


def archive_record_snapshot(snapshot_key: str, data: bytes, content_type: str = "application/json") -> Dict[str, Any]:
    s3 = boto3.client("s3")
    s3.put_object(Bucket=S3_BUCKET, Key=snapshot_key, Body=data, ContentType=content_type)
    return {"provider": "Amazon S3", "bucket": S3_BUCKET, "key": snapshot_key, "archived": True}
