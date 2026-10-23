import os
import json
import boto3
from typing import Dict, Any


def archive_record(record: Dict[str, Any]) -> str:
    """
    Archives a document snapshot to Amazon S3.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    bucket_name = os.environ.get("S3_BUCKET_NAME")

    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME environment variable not set.")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    document_id = record.get("document_id")
    if not document_id:
        raise ValueError("Record must have a 'document_id'.")

    file_key = f"archive/{document_id}.json"

    s3_client.put_object(
        Bucket=bucket_name, Key=file_key, Body=json.dumps(record, indent=4)
    )

    return f"s3://{bucket_name}/{file_key}"
