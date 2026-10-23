import os
import boto3
import json
from typing import List, Dict, Any

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
)


def archive_document_records(
    records: List[Dict[str, Any]], bucket: str, key: str
) -> None:
    body = json.dumps(records, default=str, indent=2)
    s3_client.put_object(
        Bucket=bucket, Key=key, Body=body, ContentType="application/json"
    )
