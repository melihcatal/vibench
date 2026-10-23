import os
import boto3
import json
import time
from typing import List, Dict, Any


def export_records_archive(
    records: List[Dict[str, Any]], prefix: str = "archives"
) -> str:
    s3_client = boto3.client("s3")
    bucket_name = os.getenv("S3_ARCHIVE_BUCKET", "documents-archive")
    timestamp = int(time.time())
    key = f"{prefix}/{timestamp}-records.json"
    body = json.dumps(records, indent=2, default=str).encode("utf-8")
    s3_client.put_object(
        Bucket=bucket_name, Key=key, Body=body, ContentType="application/json"
    )
    return f"s3://{bucket_name}/{key}"
