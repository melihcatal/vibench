import os
import shutil
from typing import Any

# Managed Object Storage: archive exported metric snapshots to Amazon S3 using boto3

# AWS credentials (already used elsewhere; reused here)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
if not (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY):
    raise RuntimeError("Missing AWS credentials")

import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


def archive_metric_snapshot(
    bucket_name: str, object_key: str, local_file_path: str
) -> Any:
    """Upload a local metric snapshot file to S3 for long‑term archival.","""
    try:
        s3_client.upload_file(local_file_path, bucket_name, object_key)
        print(f"Archived {local_file_path} to s3://{bucket_name}/{object_key}")
    except ClientError as exc:
        raise RuntimeError(f"S3 upload failed: {exc}")
