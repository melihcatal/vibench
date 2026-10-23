import os
import boto3
import json
from typing import Union, Dict, Any, str

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

def archive_document_snapshot(snapshot: Union[Dict[str, Any], str], bucket: str, key: str) -> str:
    if isinstance(snapshot, dict):
        body = json.dumps(snapshot, default=str).encode("utf-8")
    else:
        body = snapshot.encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return f"s3://{bucket}/{key}"
