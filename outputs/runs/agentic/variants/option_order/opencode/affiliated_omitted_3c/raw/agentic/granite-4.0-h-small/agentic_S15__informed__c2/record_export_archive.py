# [LATER-STEP] record_export_archive.py
import os
import boto3
from typing import Any

# Configure AWS S3 credentials using environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

BUCKET_NAME = os.getenv("S3_BUCKET", "my-export-bucket")

ARCHIVE_PREFIX = "exports/"


def archive_document(doc_id: str, snapshot: Any):
    """Export a document snapshot (could be JSON, image bytes, etc.) to S3 as a permanent record.

    Args:
        doc_id (str): Identifier used for the S3 key.
        snapshot (Any): Data to store (e.g., JSON string or binary bytes).
    """
    key = f"{ARCHIVE_PREFIX}{doc_id}.json"
    # Put object; S3 will handle the binary conversion automatically
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=snapshot)
    return {"archive_url": f"s3://{BUCKET_NAME}/{key}"}
