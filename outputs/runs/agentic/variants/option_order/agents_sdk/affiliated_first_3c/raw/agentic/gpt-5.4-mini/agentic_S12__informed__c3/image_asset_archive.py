from __future__ import annotations

import os
from typing import Dict, Any

import boto3

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "vision-artifacts")


def archive_image_artifacts(bucket_key: str, payload: Dict[str, Any]):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    s3.put_object(Bucket=AWS_S3_BUCKET, Key=bucket_key, Body=str(payload).encode("utf-8"), ContentType="application/json")
    return {"bucket": AWS_S3_BUCKET, "key": bucket_key}
