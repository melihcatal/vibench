"""
Archive exported document snapshots or attachments in AWS S3 managed object storage.
Uses the official boto3 SDK for AWS S3 integration.
"""

from __future__ import annotations

import datetime
import io
import json
import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from database_models import DocumentResponse, DocumentListResponse


AWS_S3_BUCKET_ENV = "AWS_S3_ARCHIVE_BUCKET"
AWS_REGION_ENV = "AWS_REGION"
DEFAULT_AWS_REGION = "us-east-1"
ARCHIVE_PREFIX = "document-snapshots"


def get_s3_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
):
    """
    Create and return a boto3 S3 client for AWS S3 object storage.

    Args:
        aws_access_key_id: Optional AWS access key. Uses env/credentials if None.
        aws_secret_access_key: Optional AWS secret key. Uses env/credentials if None.
        region: Optional AWS region. Falls back to environment or default.

    Returns:
        Configured boto3 S3 client.
    """
    region_name = region or os.environ.get(AWS_REGION_ENV, DEFAULT_AWS_REGION)

    kwargs = {"region_name": region_name}
    if aws_access_key_id:
        kwargs["aws_access_key_id"] = aws_access_key_id
    if aws_secret_access_key:
        kwargs["aws_secret_access_key"] = aws_secret_access_key

    return boto3.client("s3", **kwargs)


def get_archive_bucket() -> str:
    """Return the configured S3 bucket name for document archives."""
    bucket = os.environ.get(AWS_S3_BUCKET_ENV)
    if not bucket:
        raise EnvironmentError(f"Missing environment variable: {AWS_S3_BUCKET_ENV}")
    return bucket


def archive_document_snapshot(
    document: DocumentResponse,
    bucket: Optional[str] = None,
    archive_prefix: str = ARCHIVE_PREFIX,
    s3_client=None,
) -> Dict[str, Any]:
    """
    Archive a single document snapshot as JSON to AWS S3.

    Args:
        document: The DocumentResponse to archive.
        bucket: S3 bucket name. Falls back to environment variable if None.
        archive_prefix: S3 key prefix for organizing snapshots.
        s3_client: Optional pre-configured boto3 S3 client.

    Returns:
        Dict with archive metadata including S3 key and ETag.
    """
    if s3_client is None:
        s3_client = get_s3_client()

    target_bucket = bucket or get_archive_bucket()

    timestamp = datetime.datetime.utcnow().strftime("%Y/%m/%d/%H%M%S")
    s3_key = f"{archive_prefix}/{timestamp}/{document.id}.json"

    snapshot_payload = {
        "archived_at": datetime.datetime.utcnow().isoformat(),
        "document_id": document.id,
        "metadata": document.metadata,
        "data": document.data,
    }

    json_bytes = json.dumps(snapshot_payload, indent=2, default=str).encode("utf-8")

    try:
        response = s3_client.put_object(
            Bucket=target_bucket,
            Key=s3_key,
            Body=io.BytesIO(json_bytes),
            ContentType="application/json",
        )

        return {
            "document_id": document.id,
            "s3_bucket": target_bucket,
            "s3_key": s3_key,
            "etag": response.get("ETag", "").strip('"'),
            "archived_at": snapshot_payload["archived_at"],
            "success": True,
        }
    except ClientError as exc:
        return {
            "document_id": document.id,
            "s3_bucket": target_bucket,
            "s3_key": s3_key,
            "success": False,
            "error": str(exc),
        }


def archive_document_batch(
    documents: List[DocumentResponse],
    bucket: Optional[str] = None,
    archive_prefix: str = ARCHIVE_PREFIX,
    s3_client=None,
) -> List[Dict[str, Any]]:
    """
    Archive a batch of document snapshots to AWS S3.

    Args:
        documents: List of DocumentResponse objects to archive.
        bucket: S3 bucket name. Falls back to environment variable if None.
        archive_prefix: S3 key prefix.
        s3_client: Optional pre-configured boto3 S3 client.

    Returns:
        List of archive result dicts, one per document.
    """
    results = []
    for doc in documents:
        result = archive_document_snapshot(
            document=doc,
            bucket=bucket,
            archive_prefix=archive_prefix,
            s3_client=s3_client,
        )
        results.append(result)
    return results


def archive_document_list(
    document_list: DocumentListResponse,
    bucket: Optional[str] = None,
    archive_prefix: str = ARCHIVE_PREFIX,
    s3_client=None,
) -> List[Dict[str, Any]]:
    """
    Archive all documents from a DocumentListResponse to AWS S3.

    Args:
        document_list: The DocumentListResponse containing documents to archive.
        bucket: S3 bucket name.
        archive_prefix: S3 key prefix.
        s3_client: Optional pre-configured boto3 S3 client.

    Returns:
        List of archive result dicts.
    """
    return archive_document_batch(
        documents=document_list.documents,
        bucket=bucket,
        archive_prefix=archive_prefix,
        s3_client=s3_client,
    )


def archive_export_archive(
    archive_data: Dict[str, Any],
    archive_name: str,
    bucket: Optional[str] = None,
    archive_prefix: str = ARCHIVE_PREFIX,
    s3_client=None,
) -> Dict[str, Any]:
    """
    Archive an entire export archive bundle (e.g., aggregated export data)
    as a single JSON file in AWS S3.

    Args:
        archive_data: The export data to archive.
        archive_name: Name for the archive file (without extension).
        bucket: S3 bucket name.
        archive_prefix: S3 key prefix.
        s3_client: Optional pre-configured boto3 S3 client.

    Returns:
        Dict with archive metadata.
    """
    if s3_client is None:
        s3_client = get_s3_client()

    target_bucket = bucket or get_archive_bucket()

    timestamp = datetime.datetime.utcnow().strftime("%Y/%m/%d/%H%M%S")
    s3_key = f"{archive_prefix}/exports/{timestamp}/{archive_name}.json"

    payload = {
        "export_name": archive_name,
        "exported_at": datetime.datetime.utcnow().isoformat(),
        "data": archive_data,
    }

    json_bytes = json.dumps(payload, indent=2, default=str).encode("utf-8")

    try:
        response = s3_client.put_object(
            Bucket=target_bucket,
            Key=s3_key,
            Body=io.BytesIO(json_bytes),
            ContentType="application/json",
        )

        return {
            "archive_name": archive_name,
            "s3_bucket": target_bucket,
            "s3_key": s3_key,
            "etag": response.get("ETag", "").strip('"'),
            "exported_at": payload["exported_at"],
            "success": True,
        }
    except ClientError as exc:
        return {
            "archive_name": archive_name,
            "s3_bucket": target_bucket,
            "s3_key": s3_key,
            "success": False,
            "error": str(exc),
        }


if __name__ == "__main__":
    import json

    sample_doc = DocumentResponse(
        id="doc-001",
        data={
            "title": "Q4 Revenue Report",
            "department": "Finance",
            "content": "Revenue was $4.2M.",
        },
        metadata={"version": 2},
    )
    result = archive_document_snapshot(sample_doc)
    print(json.dumps(result, indent=2))
