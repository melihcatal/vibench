import os
import json
import boto3
from typing import List, Dict, Any
from datetime import datetime

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

def record_export_archive(records: List[Dict[str, Any]], bucket: str, prefix: str = "archives"):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    key = f"{prefix}/records_{timestamp}.json"
    body = json.dumps(records, indent=2, default=str).encode("utf-8")
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType="application/json"
    )