"""
Archive exported document snapshots or attachments in AWS S3 managed object storage.
"""

import io
import json
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
S3_BUCKET = os.environ.get("DOCUMENT_ARCHIVE_BUCKET", "document-archives")
S3_PREFIX = os.environ.get("DOCUMENT_ARCHIVE_PREFIX", "snapshots")


def get_s3_client():
    """Return a boto3 S3 client."""
    return boto3.client("s3", region_name=AWS_REGION)


def archive_document_snapshot(
    document_id: str,
    document_data: dict,
    s3_bucket: str | None = None,
    s3_prefix: str | None = None,
) -> dict:
    """
    Serialize a document record as JSON and upload it to AWS S3 for archival.

    Parameters
    ----------
    document_id : str
        Unique identifier for the document being archived.
    document_data : dict
        The document record to archive.
    s3_bucket : str, optional
        S3 bucket name.  Defaults to ``S3_BUCKET`` environment variable.
    s3_prefix : str, optional
        S3 key prefix.  Defaults to ``S3_PREFIX`` environment variable.

    Returns
    -------
    dict
        Archive metadata including ``s3_uri``, ``etag``, and ``archived_at`` timestamp.
    """
    client = get_s3_client()
    bucket = s3_bucket or S3_BUCKET
    prefix = s3_prefix or S3_PREFIX

    timestamp = datetime.now(timezone.utc)
    date_part = timestamp.strftime("%Y/%m/%d")
    key = f"{prefix}/{date_part}/{document_id}.json"

    payload = json.dumps(document_data, default=str, ensure_ascii=False).encode("utf-8")

    try:
        response = client.put_object(
            Bucket=bucket,
            Key=key,
            Body=io.BytesIO(payload),
            ContentType="application/json",
            Metadata={
                "document_id": document_id,
                "archived_at": timestamp.isoformat(),
            },
        )
        return {
            "document_id": document_id,
            "s3_uri": f"s3://{bucket}/{key}",
            "bucket": bucket,
            "key": key,
            "etag": response.get("ETag", "").strip('"'),
            "archived_at": timestamp.isoformat(),
        }
    except (BotoCoreError, ClientError) as exc:
        return {
            "document_id": document_id,
            "s3_uri": f"s3://{bucket}/{key}",
            "bucket": bucket,
            "key": key,
            "archived_at": timestamp.isoformat(),
            "error": str(exc),
        }


def archive_multiple_snapshots(
    documents: list[dict],
    s3_bucket: str | None = None,
    s3_prefix: str | None = None,
) -> list[dict]:
    """
    Archive a batch of document snapshots to AWS S3.

    Parameters
    ----------
    documents : list[dict]
        Document records to archive.  Each must have a ``document_id`` field.
    s3_bucket : str, optional
        Override S3 bucket.
    s3_prefix : str, optional
        Override S3 key prefix.

    Returns
    -------
    list[dict]
        One archive metadata dict per input document.
    """
    results = []
    for doc in documents:
        doc_id = doc.get("document_id")
        if doc_id is None:
            results.append({
                "document_id": None,
                "error": "Missing document_id field",
                "archived_at": datetime.now(timezone.utc).isoformat(),
            })
            continue
        results.append(archive_document_snapshot(doc_id, doc, s3_bucket, s3_prefix))
    return results
