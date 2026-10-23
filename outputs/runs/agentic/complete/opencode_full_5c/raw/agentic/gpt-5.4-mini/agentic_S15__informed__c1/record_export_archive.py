from io import BytesIO
from typing import Any, Dict

import boto3

from database_client import get_settings


def archive_record_snapshot(record: Dict[str, Any], key: str) -> str:
    s3 = boto3.client("s3")
    bucket = get_settings()["archive_bucket"]
    body = BytesIO(str(record).encode("utf-8"))
    s3.upload_fileobj(body, bucket, key)
    return f"s3://{bucket}/{key}"
