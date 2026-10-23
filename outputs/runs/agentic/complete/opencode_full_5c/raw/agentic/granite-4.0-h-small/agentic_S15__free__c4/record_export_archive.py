# [LATER-STEP] record_export_archive.py
"""Archive exported document snapshots or attachments in managed object storage.

Uses Amazon S3 (boto3) via the helper `database_client.py`. The function
receives a document identifier and a binary payload (e.g., a JSON snapshot,
PDF, or image). It uploads the payload to a versioned S3 bucket, using a
key pattern based on the document ID and current timestamp.
"""

import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

from database_client import get_s3_client


def export_snapshot(
    bucket_name: str, document_id: str, snapshot_id: str, data: bytes
) -> bool:
    """Upload a document snapshot/attachment to S3 and return True on success.

    Args:
        bucket_name: Target S3 bucket for archived data.
        document_id: Primary identifier of the document.
        snapshot_id: Human‑readable identifier for this particular snapshot.
        data: Raw bytes of the snapshot/attachment.

    The object key will be `documents/{document_id}/{snapshot_id}_{timestamp}`.
    """
    client = get_s3_client()
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    key = f"documents/{document_id}/{snapshot_id}_{timestamp}.bin"
    try:
        client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=data,
            # Enable server‑side encryption and versioning automatically if bucket
            # has those features configured.
        )
        return True
    except ClientError as e:
        print(f"S3 upload failed for {key}: {e}")
        return False
