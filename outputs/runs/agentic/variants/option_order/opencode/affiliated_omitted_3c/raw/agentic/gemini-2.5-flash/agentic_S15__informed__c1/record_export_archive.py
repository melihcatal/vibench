import os
import boto3
from typing import Dict, Any


def record_export_archive(
    document_id: str, document_snapshot: bytes, bucket_name: str
) -> Dict[str, Any]:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region_name = os.environ.get("AWS_REGION", "us-east-1")  # Default region

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in environment variables."
        )

    s3_client = boto3.client(
        "s3",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    object_key = f"archives/{document_id}.json"

    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=document_snapshot)

    return {
        "bucket": bucket_name,
        "key": object_key,
        "message": "Document archived successfully.",
    }
