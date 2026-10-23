import os
import boto3
import json
from database_models import Document

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ.get("AWS_REGION", "us-east-1")
)

def record_export_archive(document: Document, bucket: str, key_prefix: str = "archives/") -> str:
    import time
    timestamp = document.get("updated_at", time.time())
    if isinstance(timestamp, str):
        pass
    else:
        timestamp = str(timestamp)
    key = f"{key_prefix}{document.get('_id', 'unknown')}_{timestamp}.json"
    body = json.dumps(document, default=str).encode("utf-8")
    s3_client.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return key