import os
import boto3
import json
from typing import Dict, Any


def archive_document_to_s3(document: Dict[str, Any], doc_id: str):
    bucket_name = os.environ.get("S3_ARCHIVE_BUCKET")
    if not bucket_name:
        raise ValueError("S3_ARCHIVE_BUCKET environment variable not set.")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )
    object_key = f"documents-archive/{doc_id}.json"

    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(document, indent=2).encode("utf-8"),
        ContentType="application/json",
    )

    return {"bucket": bucket_name, "key": object_key}
