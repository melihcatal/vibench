import os
import json
import boto3
from typing import List, Dict, Any

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
)


def archive_records_to_s3(
    records: List[Dict[str, Any]], bucket_name: str, object_key: str
) -> bool:
    content = json.dumps(records, indent=2, default=str)
    response = s3_client.put_object(
        Bucket=bucket_name, Key=object_key, Body=content, ContentType="application/json"
    )
    return response["ResponseMetadata"]["HTTPStatusCode"] == 200
