import os
from typing import Any, Dict

import boto3

BUCKET_NAME = os.environ["AWS_S3_BUCKET"]


def archive_snapshot(key: str, content: bytes) -> Dict[str, Any]:
    s3 = boto3.client("s3")
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=content)
    return {"bucket": BUCKET_NAME, "key": key}
