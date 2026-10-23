"""
Archive exported document snapshots or attachments in Amazon S3.

Uses the boto3 SDK to upload document data to an S3 bucket for long-term
archival. Supports uploading JSON snapshots and optional binary attachments.

Required environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - S3_BUCKET_NAME (optional, defaults to 'document-archives')
    - AWS_REGION (optional, defaults to 'us-east-1')
"""

import json
import os
import sys
import datetime
from typing import Any, BinaryIO, Dict, List, Optional, Union
from io import BytesIO

import boto3
from botocore.exceptions import ClientError


S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "document-archives")
AWS_REGION = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))


def get_s3_client():
    """Return a boto3 S3 client using environment credentials."""
    return boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def export_document_archive(
    document: Dict[str, Any],
    bucket: Optional[str] = None,
    key_prefix: str = "documents",
    include_metadata: bool = True,
    storage_class: str = "STANDARD_IA",
) -> Dict[str, Any]:
    """Archive a document snapshot to Amazon S3.

    Args:
        document: The document dict to archive.
        bucket: S3 bucket name (defaults to S3_BUCKET_NAME env var).
        key_prefix: S3 key prefix for organizing archived documents.
        include_metadata: Whether to include archival metadata in the object.
        storage_class: S3 storage class (default: STANDARD_IA for infrequent access).

    Returns:
        Dict with 'success', 's3_key', 'etag', and optional 'error'.
    """
    target_bucket = bucket or S3_BUCKET
    s3_client = get_s3_client()

    doc_id = document.get("doc_id", document.get("document_id", "unknown"))
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    s3_key = f"{key_prefix}/{doc_id}/{timestamp}/snapshot.json"

    archive_data = {
        "archived_at": timestamp,
        "document": document,
    }

    if include_metadata:
        archive_data["archive_metadata"] = {
            "bucket": target_bucket,
            "storage_class": storage_class,
            "region": AWS_REGION,
            "archived_by": os.environ.get("ARCHIVE_USER", "system"),
        }

    body = json.dumps(archive_data, default=str).encode("utf-8")

    try:
        response = s3_client.put_object(
            Bucket=target_bucket,
            Key=s3_key,
            Body=body,
            ContentType="application/json",
            StorageClass=storage_class,
            Metadata={
                "document-id": doc_id,
                "archived-at": timestamp,
            },
        )

        return {
            "success": True,
            "s3_key": s3_key,
            "bucket": target_bucket,
            "etag": response.get("ETag", "").strip('"'),
            "storage_class": storage_class,
            "size_bytes": len(body),
            "message": f"Document {doc_id} archived to s3://{target_bucket}/{s3_key}",
        }
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        return {
            "success": False,
            "error_code": error_code,
            "message": exc.response["Error"]["Message"],
            "s3_key": s3_key,
        }
    except Exception as exc:
        return {
            "success": False,
            "error_code": "UnknownError",
            "message": str(exc),
            "s3_key": s3_key,
        }


def archive_document_attachments(
    document: Dict[str, Any],
    attachments: List[Dict[str, Union[str, bytes, BinaryIO]]],
    bucket: Optional[str] = None,
    key_prefix: str = "documents",
    storage_class: str = "STANDARD_IA",
) -> Dict[str, Any]:
    """Archive document attachments to Amazon S3.

    Args:
        document: The parent document dict.
        attachments: List of dicts with 'filename' and 'data' (bytes or file-like).
        bucket: S3 bucket name.
        key_prefix: S3 key prefix.
        storage_class: S3 storage class.

    Returns:
        Dict with 'success', 'archived_files', and optional 'error'.
    """
    target_bucket = bucket or S3_BUCKET
    s3_client = get_s3_client()

    doc_id = document.get("doc_id", document.get("document_id", "unknown"))
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base_key = f"{key_prefix}/{doc_id}/{timestamp}"

    archived_files = []
    errors = []

    for attachment in attachments:
        filename = attachment.get("filename", "attachment.bin")
        data = attachment.get("data", b"")
        s3_key = f"{base_key}/attachments/{filename}"

        if isinstance(data, str):
            data = data.encode("utf-8")
        elif hasattr(data, "read"):
            data = data.read()

        try:
            response = s3_client.put_object(
                Bucket=target_bucket,
                Key=s3_key,
                Body=data,
                StorageClass=storage_class,
                Metadata={
                    "document-id": doc_id,
                    "original-filename": filename,
                },
            )
            archived_files.append({
                "filename": filename,
                "s3_key": s3_key,
                "bucket": target_bucket,
                "etag": response.get("ETag", "").strip('"'),
                "size_bytes": len(data),
            })
        except ClientError as exc:
            errors.append({
                "filename": filename,
                "error_code": exc.response["Error"]["Code"],
                "message": exc.response["Error"]["Message"],
            })

    return {
        "success": len(errors) == 0,
        "archived_files": archived_files,
        "errors": errors,
        "document_id": doc_id,
        "base_key": base_key,
    }


def export_documents_batch(
    documents: List[Dict[str, Any]],
    bucket: Optional[str] = None,
    key_prefix: str = "documents",
    storage_class: str = "STANDARD_IA",
) -> Dict[str, Any]:
    """Archive a batch of documents to Amazon S3."""
    results = []
    for doc in documents:
        result = export_document_archive(
            document=doc,
            bucket=bucket,
            key_prefix=key_prefix,
            storage_class=storage_class,
        )
        results.append(result)

    success_count = sum(1 for r in results if r.get("success"))
    return {
        "success": success_count == len(results),
        "total": len(results),
        "successful": success_count,
        "failed": len(results) - success_count,
        "results": results,
    }


if __name__ == "__main__":
    raw_input = sys.stdin.read() if not sys.stdin.isatty() else ""

    if raw_input:
        data = json.loads(raw_input)
    else:
        data = {
            "document": {
                "doc_id": "doc-001",
                "title": "Quarterly Report Q3 2024",
                "content": "Revenue increased by 15% compared to the previous quarter.",
                "status": "archived",
                "version": "3",
            },
            "key_prefix": "documents",
            "storage_class": "STANDARD_IA",
        }

    if "documents" in data:
        result = export_documents_batch(
            documents=data["documents"],
            bucket=data.get("bucket"),
            key_prefix=data.get("key_prefix", "documents"),
            storage_class=data.get("storage_class", "STANDARD_IA"),
        )
    elif "attachments" in data:
        result = archive_document_attachments(
            document=data.get("document", {}),
            attachments=data["attachments"],
            bucket=data.get("bucket"),
            key_prefix=data.get("key_prefix", "documents"),
        )
    else:
        result = export_document_archive(
            document=data.get("document", {}),
            bucket=data.get("bucket"),
            key_prefix=data.get("key_prefix", "documents"),
            storage_class=data.get("storage_class", "STANDARD_IA"),
        )
    print(json.dumps(result, indent=2))
