import os
import json
import boto3
from typing import List, Dict, Any
from io import BytesIO


def record_export_archive(
    records: List[Dict[str, Any]], bucket_name: str, object_key: str
) -> None:
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not access_key or not secret_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set.")
    s3_client = boto3.client(
        "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )
    archive_data = json.dumps(records, indent=2, default=str)
    body = BytesIO(archive_data.encode("utf-8"))
    s3_client.put_object(
        Bucket=bucket_name, Key=object_key, Body=body, ContentType="application/json"
    )
