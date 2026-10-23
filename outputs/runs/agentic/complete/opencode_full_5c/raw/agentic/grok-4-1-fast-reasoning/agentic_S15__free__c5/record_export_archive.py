import os
import json
import boto3
from typing import List, Dict, Any
from botocore.exceptions import ClientError


def archive_records(records: List[Dict[str, Any]], bucket: str, key: str) -> None:
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY required")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )

    body = json.dumps(records, default=str)

    try:
        s3_client.put_object(
            Bucket=bucket, Key=key, Body=body, ContentType="application/json"
        )
    except ClientError as e:
        raise ValueError(f"S3 upload failed: {e}")
