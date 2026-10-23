import os
import json
import boto3
from typing import List, Dict, Any
from botocore.exceptions import NoCredentialsError, ClientError


def archive_records_to_s3(
    records: List[Dict[str, Any]], bucket_name: str, object_key: str
):
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials environment variables are required.")
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )
    body = json.dumps(records, default=str, indent=2).encode("utf-8")
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=body,
            ContentType="application/json",
        )
    except ClientError as e:
        raise RuntimeError(f"Failed to upload to S3: {e}")
