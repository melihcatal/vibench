"""
Archive exported document snapshots or attachments in AWS S3 managed object storage.
Uses the boto3 AWS SDK for Amazon S3 integration.
"""

from __future__ import annotations

import gzip
import io
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError

AWS_REGION_ENV = "AWS_DEFAULT_REGION"
DEFAULT_S3_BUCKET_NAME = "document-store-archives"
S3_ARCHIVE_PREFIX = "document-exports"


def _get_s3_client() -> boto3.client:
    """Create and return a boto3 client for Amazon S3."""
    region = os.environ.get(AWS_REGION_ENV, "us-east-1")
    return boto3.client("s3", region_name=region)


def archive_document_snapshot(
    document: dict[str, Any],
    bucket_name: str = DEFAULT_S3_BUCKET_NAME,
    s3_key: Optional[str] = None,
    client: Optional[Any] = None,
    metadata: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    """
    Archive a single document snapshot as a JSON object in Amazon S3.
    
    Args:
        document: The document record dict to archive.
        bucket_name: The target S3 bucket name.
        s3_key: Optional S3 object key. If None, one is auto-generated.
        client: Optional pre-configured boto3 S3 client.
        metadata: Optional S3 user metadata dict.
    
    Returns:
        A dict with the S3 bucket, key, and ETag of the archived object.
    """
    if client is None:
        client = _get_s3_client()

    if s3_key is None:
        doc_id = document.get("doc_id", "unknown")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        s3_key = f"{S3_ARCHIVE_PREFIX}/{doc_id}/{timestamp}.json"

    json_payload = json.dumps(document, indent=2, default=str).encode("utf-8")

    upload_metadata: dict[str, str] = {
        "doc-id": document.get("doc_id", ""),
        "archived-at": datetime.now(timezone.utc).isoformat(),
    }
    if metadata:
        upload_metadata.update(metadata)

    try:
        response = client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json_payload,
            ContentType="application/json",
            Metadata=upload_metadata,
        )
        return {
            "bucket": bucket_name,
            "key": s3_key,
            "etag": response.get("ETag", "").strip('"'),
            "version_id": response.get("VersionId"),
            "archived_at": upload_metadata["archived-at"],
        }
    except ClientError as e:
        raise RuntimeError(f"Amazon S3 archive upload failed: {e}")


def archive_document_snapshot_gzipped(
    document: dict[str, Any],
    bucket_name: str = DEFAULT_S3_BUCKET_NAME,
    s3_key: Optional[str] = None,
    client: Optional[Any] = None,
) -> dict[str, Any]:
    """
    Archive a document snapshot as a gzip-compressed JSON object in Amazon S3.
    
    Args:
        document: The document record dict to archive.
        bucket_name: The target S3 bucket name.
        s3_key: Optional S3 object key. If None, one is auto-generated.
        client: Optional pre-configured boto3 S3 client.
    
    Returns:
        A dict with the S3 bucket, key, and ETag of the archived object.
    """
    if client is None:
        client = _get_s3_client()

    if s3_key is None:
        doc_id = document.get("doc_id", "unknown")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        s3_key = f"{S3_ARCHIVE_PREFIX}/{doc_id}/{timestamp}.json.gz"

    json_payload = json.dumps(document, indent=2, default=str).encode("utf-8")
    gzipped_buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=gzipped_buffer, mode="wb") as gz:
        gz.write(json_payload)
    gzipped_buffer.seek(0)

    try:
        response = client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=gzipped_buffer.getvalue(),
            ContentType="application/gzip",
            Metadata={
                "doc-id": document.get("doc_id", ""),
                "archived-at": datetime.now(timezone.utc).isoformat(),
                "compression": "gzip",
            },
        )
        return {
            "bucket": bucket_name,
            "key": s3_key,
            "etag": response.get("ETag", "").strip('"'),
            "version_id": response.get("VersionId"),
            "compression": "gzip",
        }
    except ClientError as e:
        raise RuntimeError(f"Amazon S3 gzipped archive upload failed: {e}")


def batch_archive_documents(
    documents: list[dict[str, Any]],
    bucket_name: str = DEFAULT_S3_BUCKET_NAME,
    client: Optional[Any] = None,
    gzip_compress: bool = False,
) -> list[dict[str, Any]]:
    """
    Archive multiple document snapshots to Amazon S3.
    
    Args:
        documents: A list of document record dicts to archive.
        bucket_name: The target S3 bucket name.
        client: Optional pre-configured boto3 S3 client.
        gzip_compress: Whether to gzip-compress the JSON payloads.
    
    Returns:
        A list of archive result dicts, one per document.
    """
    results = []
    for doc in documents:
        if gzip_compress:
            result = archive_document_snapshot_gzipped(doc, bucket_name, client=client)
        else:
            result = archive_document_snapshot(doc, bucket_name, client=client)
        results.append(result)
    return results


def retrieve_archived_document(
    bucket_name: str = DEFAULT_S3_BUCKET_NAME,
    s3_key: Optional[str] = None,
    client: Optional[Any] = None,
) -> Optional[dict[str, Any]]:
    """
    Retrieve an archived document snapshot from Amazon S3.
    
    Args:
        bucket_name: The S3 bucket name.
        s3_key: The S3 object key of the archived document.
        client: Optional pre-configured boto3 S3 client.
    
    Returns:
        The parsed document dict, or None if not found.
    """
    if client is None:
        client = _get_s3_client()

    try:
        response = client.get_object(Bucket=bucket_name, Key=s3_key)
        body = response["Body"].read()
        content_type = response.get("ContentType", "")

        if content_type == "application/gzip" or s3_key.endswith(".gz"):
            body = gzip.decompress(body)

        return json.loads(body.decode("utf-8"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise RuntimeError(f"Amazon S3 retrieval failed: {e}")


def list_archived_documents(
    bucket_name: str = DEFAULT_S3_BUCKET_NAME,
    prefix: str = S3_ARCHIVE_PREFIX,
    doc_id: Optional[str] = None,
    max_keys: int = 100,
    client: Optional[Any] = None,
) -> list[dict[str, Any]]:
    """
    List archived document snapshots from Amazon S3.
    
    Args:
        bucket_name: The S3 bucket name.
        prefix: The S3 key prefix to filter by.
        doc_id: Optional specific document ID to filter archived snapshots.
        max_keys: Maximum number of keys to return.
        client: Optional pre-configured boto3 S3 client.
    
    Returns:
        A list of dicts with S3 key, size, and last modified info.
    """
    if client is None:
        client = _get_s3_client()

    search_prefix = prefix
    if doc_id:
        search_prefix = f"{prefix}/{doc_id}/"

    try:
        response = client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=search_prefix,
            MaxKeys=max_keys,
        )
        contents = response.get("Contents", [])
        return [
            {
                "key": obj["Key"],
                "size": obj["Size"],
                "last_modified": obj["LastModified"].isoformat(),
                "etag": obj["ETag"].strip('"'),
            }
            for obj in contents
        ]
    except ClientError as e:
        raise RuntimeError(f"Amazon S3 list failed: {e}")


if __name__ == "__main__":
    sample_doc = {
        "doc_id": "archive-test-001",
        "content": {"title": "Archived Document", "status": "archived"},
        "version": 3,
    }
    result = archive_document_snapshot(sample_doc)
    print(result)
