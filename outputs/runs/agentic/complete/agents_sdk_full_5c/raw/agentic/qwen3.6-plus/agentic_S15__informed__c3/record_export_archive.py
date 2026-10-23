"""
[LATER-STEP] record_export_archive.py
Archive exported document snapshots or attachments in Amazon S3 managed object storage.
Provider: Amazon S3 via boto3 SDK.
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import json
import io
from typing import List, Dict, Any, Optional
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from database_models import DocumentResponse


def get_s3_client() -> boto3.client:
    """
    Create and return an Amazon S3 client using boto3.
    Credentials are sourced from AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars.
    """
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    return boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )


def archive_document_snapshot(
    document: DocumentResponse,
    bucket: str,
    prefix: str = "document-archives",
    s3_client: Optional[boto3.client] = None,
) -> str:
    """
    Archive a single document snapshot as a JSON object in Amazon S3.

    Args:
        document: The DocumentResponse to archive.
        bucket: The S3 bucket name.
        prefix: The key prefix for archived documents.
        s3_client: Optional pre-configured boto3 S3 client.

    Returns:
        The S3 object key where the snapshot was stored.
    """
    if s3_client is None:
        s3_client = get_s3_client()

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    doc_id = document.document_id
    object_key = f"{prefix}/{doc_id}/{timestamp}.json"

    snapshot = {
        "archived_at": timestamp,
        "document": document.to_dict(),
    }

    payload = json.dumps(snapshot, indent=2, default=str).encode("utf-8")

    s3_client.put_object(
        Bucket=bucket,
        Key=object_key,
        Body=payload,
        ContentType="application/json",
    )

    return object_key


def archive_documents_batch(
    documents: List[DocumentResponse],
    bucket: str,
    prefix: str = "document-archives",
    s3_client: Optional[boto3.client] = None,
) -> List[str]:
    """
    Archive multiple document snapshots to Amazon S3.

    Args:
        documents: List of DocumentResponse objects to archive.
        bucket: The S3 bucket name.
        prefix: The key prefix for archived documents.
        s3_client: Optional pre-configured boto3 S3 client.

    Returns:
        List of S3 object keys where the snapshots were stored.
    """
    keys = []
    for doc in documents:
        key = archive_document_snapshot(doc, bucket=bucket, prefix=prefix, s3_client=s3_client)
        keys.append(key)
    return keys


def archive_attachment_bytes(
    attachment_data: bytes,
    attachment_name: str,
    document_id: str,
    bucket: str,
    prefix: str = "document-archives",
    content_type: str = "application/octet-stream",
    s3_client: Optional[boto3.client] = None,
) -> str:
    """
    Archive raw attachment bytes (e.g., PDF, image) to Amazon S3.

    Args:
        attachment_data: The binary attachment content.
        attachment_name: The filename for the attachment.
        document_id: The associated document identifier.
        bucket: The S3 bucket name.
        prefix: The key prefix for attachments.
        content_type: The MIME type of the attachment.
        s3_client: Optional pre-configured boto3 S3 client.

    Returns:
        The S3 object key where the attachment was stored.
    """
    if s3_client is None:
        s3_client = get_s3_client()

    object_key = f"{prefix}/{document_id}/attachments/{attachment_name}"

    s3_client.put_object(
        Bucket=bucket,
        Key=object_key,
        Body=attachment_data,
        ContentType=content_type,
    )

    return object_key


if __name__ == "__main__":
    sample = DocumentResponse(
        document_id="doc-001",
        data={"title": "Archived Record", "body": "This document was archived."},
    )
    bucket = os.environ.get("S3_ARCHIVE_BUCKET", "my-archive-bucket")
    key = archive_document_snapshot(sample, bucket=bucket)
    print(f"Archived to S3: s3://{bucket}/{key}")
