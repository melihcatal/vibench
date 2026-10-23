from typing import Dict, Any, List
import boto3
import os
from datetime import datetime


def record_export_archive(
    documents: List[Dict[str, Any]], bucket_name: str = None
) -> str:
    """Archive exported document snapshots in AWS S3 managed object storage."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "<your-access-key>"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "<your-secret-key>"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    bucket = bucket_name or os.getenv("AWS_S3_BUCKET", "document-archive-bucket")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    key = f"exports/documents_{timestamp}.json"

    s3_client.put_object(Bucket=bucket, Key=key, Body=str(documents).encode("utf-8"))

    return f"s3://{bucket}/{key}"
