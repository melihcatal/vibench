import boto3
import os
from datetime import datetime
from typing import Dict, Optional
from .observability_client import get_client


def archive_metrics_export(
    bucket_name: str,
    file_name: str,
    data: bytes,
    region: str = "us-east-1",
) -> Dict[str, str]:
    """
    Archives exported metric snapshots in Amazon S3 managed object storage.

    Args:
        bucket_name: The name of the S3 bucket.
        file_name: The name of the file to upload.
        data: The binary data to upload.
        region: The AWS region where the bucket is located.

    Returns:
        Dict: A dictionary containing the archive operation results.
    """
    client = get_client("aws", "s3")

    client.put_object(
        Bucket=bucket_name,
        Key=f"metrics_exports/{datetime.utcnow().strftime('%Y-%m-%d')}/{file_name}",
        Body=data,
    )

    return {
        "status": "success",
        "bucket": bucket_name,
        "key": file_name,
        "timestamp": datetime.utcnow().isoformat(),
    }
