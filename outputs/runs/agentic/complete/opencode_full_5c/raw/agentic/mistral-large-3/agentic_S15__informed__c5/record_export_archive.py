import boto3
import os
import json
from datetime import datetime
from typing import Dict, Any, List


def export_documents_to_archive(
    documents: List[Dict[str, Any]],
    bucket_name: str,
    archive_prefix: str = "document_exports",
) -> Dict[str, Any]:
    """
    Archives exported document snapshots in Amazon S3.

    Args:
        documents: List of documents to archive
        bucket_name: S3 bucket name
        archive_prefix: Prefix for archive files

    Returns:
        Archive metadata including S3 paths
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_key = f"{archive_prefix}/export_{timestamp}.json"

    # Upload archive to S3
    s3_client.put_object(
        Bucket=bucket_name, Key=archive_key, Body=json.dumps(documents, indent=2)
    )

    # Generate presigned URL for temporary access
    presigned_url = s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket_name, "Key": archive_key}, ExpiresIn=3600
    )

    return {
        "archive_path": f"s3://{bucket_name}/{archive_key}",
        "presigned_url": presigned_url,
        "document_count": len(documents),
        "timestamp": timestamp,
    }
