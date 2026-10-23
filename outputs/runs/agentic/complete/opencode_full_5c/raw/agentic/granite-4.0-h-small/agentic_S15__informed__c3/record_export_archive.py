# [LATER-STEP] record_export_archive.py
# Archive exported document snapshots or attachments in Amazon S3

import os
import boto3
import uuid
import json

# S3 client configuration (environment variables for security)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


def archive_record(key, record):
    """Upload a document record (or attachment) to a private S3 bucket.

    Args:
        key (str): S3 object key (path) where the snapshot will be stored.
        record (dict): Document data to store.
    """
    BUCKET_NAME = os.getenv("AWS_S3_BUCKET")  # must be set in environment
    if not BUCKET_NAME:
        raise RuntimeError("AWS_S3_BUCKET environment variable not set")

    # Convert record to JSON string (binary upload can be added if needed)
    body = json.dumps(record, ensure_ascii=False)

    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=body.encode("utf-8"),
            ContentType="application/json",
            ACL="private",  # ensure only the account owner can access
        )
        print(f"Archived {key} to S3 bucket {BUCKET_NAME}")
    except Exception as e:
        raise RuntimeError(f"Failed to archive record: {e}")


# Example usage (uncomment for local testing):
# archive_record('snapshots/2024/08/record_123.json', {'id':'123','name':'Test'})
