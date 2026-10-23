from typing import Dict, Any, IO
import boto3
import json
import os

def archive_document(document: Dict[str, Any], bucket_name: str, object_key: str) -> str:
    s3 = boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(document).encode("utf-8")
    )
    return f"s3://{bucket_name}/{object_key}"