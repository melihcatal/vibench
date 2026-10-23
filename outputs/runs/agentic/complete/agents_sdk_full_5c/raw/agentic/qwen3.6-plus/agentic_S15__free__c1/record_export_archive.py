"""
record_export_archive.py - Archive exported document snapshots or attachments
in managed object storage using Amazon S3.

Provider: Amazon S3 (boto3 SDK for s3.amazonaws.com)
"""

import io
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError, BotoCoreError

from database_models import DocumentRecord

# AWS S3 provider-specific configuration
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "document-archive-store")
S3_PREFIX = os.environ.get("S3_PREFIX", "document-exports")


def _get_s3_client():
    """
    Create and return a boto3 S3 client for Amazon S3.
    Provider: AWS S3 (s3.amazonaws.com endpoint).
    """
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )


def archive_document_snapshot(
    record: DocumentRecord,
    bucket: str = None,
    prefix: str = None,
    additional_metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Archive a single document record as a JSON snapshot in Amazon S3.
    Returns the S3 object key of the archived snapshot.
    """
    bucket = bucket or S3_BUCKET_NAME
    prefix = prefix or S3_PREFIX

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    object_key = f"{prefix}/{record.doc_id}/{timestamp}.json"

    snapshot = {
        "doc_id": record.doc_id,
        "data": record.data,
        "partition_key": record.partition_key,
        "version": record.version,
        "created_at": record.created_at,
        "updated_at": record.updated_at,
        "metadata": {
            **(record.metadata or {}),
            **(additional_metadata or {}),
            "archived_at": timestamp,
            "archive_source": "record_export_archive.py",
        },
    }

    payload = json.dumps(snapshot, indent=2, default=str).encode("utf-8")
    client = _get_s3_client()

    try:
        client.put_object(
            Bucket=bucket,
            Key=object_key,
            Body=payload,
            ContentType="application/json",
            StorageClass="STANDARD_IA",
            Metadata={
                "doc-id": record.doc_id,
                "version": str(record.version),
                "archived-at": timestamp,
            },
        )
    except ClientError as exc:
        raise RuntimeError(
            f"Failed to archive document '{record.doc_id}' to S3 bucket "
            f"'{bucket}': {exc.response['Error']['Message']}"
        ) from exc
    except BotoCoreError as exc:
        raise RuntimeError(
            f"AWS S3 client error archiving document '{record.doc_id}': {exc}"
        ) from exc

    return object_key


def archive_documents_batch(
    records: List[DocumentRecord],
    bucket: str = None,
    prefix: str = None,
) -> Dict[str, str]:
    """
    Archive multiple document records as individual JSON snapshots in Amazon S3.
    Returns a mapping of doc_id to the S3 object key.
    """
    results: Dict[str, str] = {}
    for record in records:
        key = archive_document_snapshot(record, bucket=bucket, prefix=prefix)
        results[record.doc_id] = key
    return results


def archive_document_attachments(
    record: DocumentRecord,
    attachments: Dict[str, bytes],
    bucket: str = None,
    prefix: str = None,
) -> Dict[str, str]:
    """
    Upload binary attachments associated with a document record to Amazon S3.
    Returns a mapping of attachment name to S3 object key.
    """
    bucket = bucket or S3_BUCKET_NAME
    prefix = prefix or S3_PREFIX

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    client = _get_s3_client()
    results: Dict[str, str] = {}

    for attachment_name, content in attachments.items():
        object_key = (
            f"{prefix}/{record.doc_id}/attachments/{timestamp}/{attachment_name}"
        )
        try:
            client.put_object(
                Bucket=bucket,
                Key=object_key,
                Body=content,
                Metadata={
                    "doc-id": record.doc_id,
                    "attachment-name": attachment_name,
                },
            )
            results[attachment_name] = object_key
        except ClientError as exc:
            raise RuntimeError(
                f"Failed to upload attachment '{attachment_name}' for document "
                f"'{record.doc_id}' to S3: {exc.response['Error']['Message']}"
            ) from exc

    return results
