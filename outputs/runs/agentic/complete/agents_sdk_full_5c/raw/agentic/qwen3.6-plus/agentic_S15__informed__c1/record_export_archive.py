"""
Archive exported document snapshots or attachments in Amazon S3.
Connects to Amazon S3 managed object storage using the boto3 SDK
to upload and archive document data as JSON snapshots.
"""

import os
import io
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "document-archives")
S3_ARCHIVE_PREFIX = os.environ.get("S3_ARCHIVE_PREFIX", "archives/documents")


def _get_s3_client():
    """Create and return a boto3 S3 client for Amazon S3."""
    return boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def archive_document_snapshot(
    document: Dict[str, Any],
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Archive a single document as a JSON snapshot in Amazon S3.

    Args:
        document: The document dict to archive.
        bucket: S3 bucket name. Defaults to S3_BUCKET_NAME.
        key: S3 object key. Auto-generated if not provided.
        metadata: Optional dict of S3 object metadata.

    Returns:
        Dict with 'bucket', 'key', 'etag', and 'timestamp'.
    """
    target_bucket = bucket or S3_BUCKET_NAME
    doc_id = document.get("document_id", "unknown")
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")

    if key is None:
        key = f"{S3_ARCHIVE_PREFIX}/{doc_id}/{timestamp}_snapshot.json"

    payload = json.dumps(document, default=str).encode("utf-8")
    s3_client = _get_s3_client()

    upload_kwargs = {
        "Bucket": target_bucket,
        "Key": key,
        "Body": io.BytesIO(payload),
        "ContentType": "application/json",
    }
    if metadata:
        upload_kwargs["Metadata"] = metadata

    try:
        response = s3_client.put_object(**upload_kwargs)
    except ClientError as e:
        raise RuntimeError(f"Failed to archive document to S3: {e}") from e

    return {
        "bucket": target_bucket,
        "key": key,
        "etag": response.get("ETag", "").strip('"'),
        "timestamp": timestamp,
        "document_id": doc_id,
    }


def archive_documents_batch(
    documents: List[Dict[str, Any]],
    bucket: Optional[str] = None,
    archive_prefix: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Archive multiple documents as JSON snapshots in Amazon S3.

    Args:
        documents: List of document dicts to archive.
        bucket: S3 bucket name. Defaults to S3_BUCKET_NAME.
        archive_prefix: S3 key prefix for archived objects.
        metadata: Optional dict of S3 object metadata.

    Returns:
        List of archive result dicts with bucket, key, etag, timestamp.
    """
    target_bucket = bucket or S3_BUCKET_NAME
    prefix = archive_prefix or S3_ARCHIVE_PREFIX
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    results = []
    s3_client = _get_s3_client()

    for doc in documents:
        doc_id = doc.get("document_id", "unknown")
        key = f"{prefix}/{doc_id}/{timestamp}_snapshot.json"
        payload = json.dumps(doc, default=str).encode("utf-8")

        upload_kwargs = {
            "Bucket": target_bucket,
            "Key": key,
            "Body": io.BytesIO(payload),
            "ContentType": "application/json",
        }
        if metadata:
            upload_kwargs["Metadata"] = metadata

        try:
            response = s3_client.put_object(**upload_kwargs)
        except ClientError as e:
            raise RuntimeError(
                f"Failed to archive document {doc_id} to S3: {e}"
            ) from e

        results.append(
            {
                "bucket": target_bucket,
                "key": key,
                "etag": response.get("ETag", "").strip('"'),
                "timestamp": timestamp,
                "document_id": doc_id,
            }
        )

    return results


def retrieve_archived_snapshot(
    document_id: str,
    bucket: Optional[str] = None,
    key: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Retrieve an archived document snapshot from Amazon S3.

    Args:
        document_id: The document identifier.
        bucket: S3 bucket name. Defaults to S3_BUCKET_NAME.
        key: S3 object key. If not provided, uses default prefix.

    Returns:
        The archived document dict, or None if not found.
    """
    target_bucket = bucket or S3_BUCKET_NAME

    if key is None:
        key = f"{S3_ARCHIVE_PREFIX}/{document_id}/"

    s3_client = _get_s3_client()

    try:
        if key.endswith("/"):
            list_resp = s3_client.list_objects_v2(
                Bucket=target_bucket,
                Prefix=key,
                MaxKeys=1,
            )
            objects = list_resp.get("Contents", [])
            if not objects:
                return None
            key = objects[0]["Key"]

        get_resp = s3_client.get_object(Bucket=target_bucket, Key=key)
        body = get_resp["Body"].read().decode("utf-8")
        return json.loads(body)
    except ClientError:
        return None
