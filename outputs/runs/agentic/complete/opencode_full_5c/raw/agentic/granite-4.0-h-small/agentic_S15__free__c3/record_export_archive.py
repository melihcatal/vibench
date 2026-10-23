# record_export_archive.py
"""
Later-step integration file that archives exported document snapshots or attachments.
Uses a managed object storage service (e.g., Amazon S3) to store immutable snapshots.
"""

import os
import boto3
import uuid
from database_models import Document


def archive_document_snapshot(document: Document, snapshot_name: str) -> str:
    """Archive a document snapshot as an object in S3.

    Args:
        document (Document): Document to archive.
        snapshot_name (str): Logical name for the snapshot (e.g., '2024-08-22-initial').

    Returns:
        str: The S3 object key where the snapshot is stored.
    """
    bucket_name = os.getenv("ARCHIVE_BUCKET")
    if not bucket_name:
        raise RuntimeError("ARCHIVE_BUCKET environment variable not set")
    key = f"snapshots/{snapshot_name}/{document.id}.json"
    s3 = boto3.client("s3")
    # Store as JSON with UTF-8 encoding
    payload = {
        "id": document.id,
        "version": document.version,
        "created_at": document.created_at,
        "updated_at": document.updated_at,
        "content": document.content,
    }
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=(json.dumps(payload, ensure_ascii=False)).encode("utf-8"),
        ContentType="application/json",
        Metadata={"archived-at": str(uuid.uuid4())},
    )
    return key
