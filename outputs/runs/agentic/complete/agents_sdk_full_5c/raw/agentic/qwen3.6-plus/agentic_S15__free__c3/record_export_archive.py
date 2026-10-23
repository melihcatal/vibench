"""
record_export_archive.py - Archive exported document snapshots or attachments
in Amazon S3 managed object storage. Uses the boto3 SDK to connect to AWS S3
and store document data as JSON snapshots alongside any extracted attachments.
"""

import io
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from zipfile import ZipFile

import boto3
from botocore.exceptions import ClientError

from database_client import build_atlas_client, AtlasClientHelper
from database_models import DocumentResponse, normalize_mongo_object_id


AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET", "document-archive-bucket")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


class ArchiveRecord:
    """Represents a single archived document snapshot in S3."""

    def __init__(
        self,
        doc_id: str,
        s3_key: str,
        s3_bucket: str,
        size_bytes: int,
        archived_at: str,
    ):
        self.doc_id = doc_id
        self.s3_key = s3_key
        self.s3_bucket = s3_bucket
        self.size_bytes = size_bytes
        self.archived_at = archived_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "s3_key": self.s3_key,
            "s3_bucket": self.s3_bucket,
            "s3_url": f"https://{self.s3_bucket}.s3.{AWS_REGION}.amazonaws.com/{self.s3_key}",
            "size_bytes": self.size_bytes,
            "archived_at": self.archived_at,
        }


class ArchiveBatch:
    """Aggregated result for a batch of archived document records."""

    def __init__(self, records: List[ArchiveRecord], failed_ids: List[str]):
        self.records = records
        self.failed_ids = failed_ids

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_archived": len(self.records),
            "total_failed": len(self.failed_ids),
            "failed_ids": self.failed_ids,
            "records": [r.to_dict() for r in self.records],
        }


def _get_s3_client() -> boto3.client:
    """Create a boto3 S3 client configured for the AWS region."""
    return boto3.client("s3", region_name=AWS_REGION)


def archive_document_snapshot(
    doc_response: DocumentResponse,
    bucket: Optional[str] = None,
    prefix: str = "document_snapshots",
    s3_client: Optional[boto3.client] = None,
) -> ArchiveRecord:
    """
    Archive a single document snapshot as JSON to Amazon S3.

    Args:
        doc_response: The document to archive.
        bucket: S3 bucket name (defaults to AWS_S3_BUCKET env var).
        prefix: S3 key prefix for organizing snapshots.
        s3_client: Optional pre-configured boto3 S3 client.

    Returns:
        ArchiveRecord with S3 location details.
    """
    if s3_client is None:
        s3_client = _get_s3_client()

    bucket = bucket or AWS_S3_BUCKET
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    s3_key = f"{prefix}/{doc_response.doc_id}_{timestamp}.json"

    snapshot = {
        "doc_id": doc_response.doc_id,
        "data": doc_response.data,
        "version": doc_response.version,
        "created_at": doc_response.created_at,
        "updated_at": doc_response.updated_at,
        "archived_at": datetime.utcnow().isoformat(),
    }

    body = json.dumps(snapshot, indent=2, default=str).encode("utf-8")

    s3_client.put_object(
        Bucket=bucket,
        Key=s3_key,
        Body=body,
        ContentType="application/json",
    )

    return ArchiveRecord(
        doc_id=doc_response.doc_id,
        s3_key=s3_key,
        s3_bucket=bucket,
        size_bytes=len(body),
        archived_at=timestamp,
    )


def archive_documents_batch(
    collection_name: str,
    bucket: Optional[str] = None,
    prefix: str = "document_snapshots",
    filter_field: Optional[str] = None,
    filter_value: Optional[Any] = None,
    limit: int = 100,
    mongo_client: Optional[AtlasClientHelper] = None,
    s3_client: Optional[boto3.client] = None,
) -> ArchiveBatch:
    """
    Fetch documents from MongoDB Atlas and archive each as a JSON snapshot to Amazon S3.

    Args:
        collection_name: MongoDB Atlas collection to query.
        bucket: S3 bucket name (defaults to AWS_S3_BUCKET env var).
        prefix: S3 key prefix for organizing snapshots.
        filter_field: Optional field to filter documents by.
        filter_value: Optional value for the filter field.
        limit: Maximum documents to process.
        mongo_client: Optional pre-built AtlasClientHelper instance.
        s3_client: Optional pre-configured boto3 S3 client.

    Returns:
        ArchiveBatch with archived records and any failures.
    """
    if mongo_client is None:
        mongo_client = build_atlas_client()
    if s3_client is None:
        s3_client = _get_s3_client()

    collection = mongo_client.get_collection(collection_name)

    query = {}
    if filter_field and filter_value is not None:
        query[filter_field] = filter_value

    cursor = collection.find(query).limit(limit)

    records: List[ArchiveRecord] = []
    failed_ids: List[str] = []

    for raw_doc in cursor:
        raw_doc = normalize_mongo_object_id(raw_doc)
        doc_id = str(raw_doc.get("_id", ""))
        data = raw_doc.get("data", {})
        doc_resp = DocumentResponse(
            doc_id=doc_id,
            data=data,
            version=raw_doc.get("version"),
            created_at=raw_doc.get("created_at"),
            updated_at=raw_doc.get("updated_at"),
        )
        try:
            record = archive_document_snapshot(
                doc_resp,
                bucket=bucket,
                prefix=prefix,
                s3_client=s3_client,
            )
            records.append(record)
        except ClientError as e:
            failed_ids.append(doc_id)

    return ArchiveBatch(records=records, failed_ids=failed_ids)


def archive_documents_as_zip(
    collection_name: str,
    zip_key: Optional[str] = None,
    bucket: Optional[str] = None,
    prefix: str = "document_archives",
    filter_field: Optional[str] = None,
    filter_value: Optional[Any] = None,
    limit: int = 100,
    mongo_client: Optional[AtlasClientHelper] = None,
    s3_client: Optional[boto3.client] = None,
) -> ArchiveRecord:
    """
    Fetch documents from MongoDB Atlas and archive them as a single ZIP to Amazon S3.

    Args:
        collection_name: MongoDB Atlas collection to query.
        zip_key: Optional S3 key for the zip file.
        bucket: S3 bucket name (defaults to AWS_S3_BUCKET env var).
        prefix: S3 key prefix for organizing zip archives.
        filter_field: Optional field to filter documents by.
        filter_value: Optional value for the filter field.
        limit: Maximum documents to process.
        mongo_client: Optional pre-built AtlasClientHelper instance.
        s3_client: Optional pre-configured boto3 S3 client.

    Returns:
        ArchiveRecord pointing to the zip file in S3.
    """
    if mongo_client is None:
        mongo_client = build_atlas_client()
    if s3_client is None:
        s3_client = _get_s3_client()

    bucket = bucket or AWS_S3_BUCKET

    collection = mongo_client.get_collection(collection_name)

    query = {}
    if filter_field and filter_value is not None:
        query[filter_field] = filter_value

    cursor = collection.find(query).limit(limit)

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    if zip_key is None:
        zip_key = f"{prefix}/documents_{timestamp}.zip"

    buf = io.BytesIO()
    doc_count = 0

    with ZipFile(buf, "w") as zf:
        for raw_doc in cursor:
            raw_doc = normalize_mongo_object_id(raw_doc)
            doc_id = str(raw_doc.get("_id", ""))
            data = raw_doc.get("data", {})
            snapshot = {
                "doc_id": doc_id,
                "data": data,
                "version": raw_doc.get("version"),
                "created_at": raw_doc.get("created_at"),
                "updated_at": raw_doc.get("updated_at"),
                "archived_at": datetime.utcnow().isoformat(),
            }
            json_bytes = json.dumps(snapshot, indent=2, default=str).encode("utf-8")
            zf.writestr(f"{doc_id}.json", json_bytes)
            doc_count += 1

    buf.seek(0)
    body = buf.read()

    s3_client.put_object(
        Bucket=bucket,
        Key=zip_key,
        Body=body,
        ContentType="application/zip",
    )

    return ArchiveRecord(
        doc_id="batch",
        s3_key=zip_key,
        s3_bucket=bucket,
        size_bytes=len(body),
        archived_at=timestamp,
    )


if __name__ == "__main__":
    batch = archive_documents_batch(
        collection_name="documents",
        limit=10,
    )
    print(json.dumps(batch.to_dict(), indent=2, default=str))
