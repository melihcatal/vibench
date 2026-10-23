import os
import json
import hashlib
import io
import gzip
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "document-archive-bucket")
S3_ARCHIVE_PREFIX = os.environ.get("S3_ARCHIVE_PREFIX", "document-snapshots")


def _get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )


def _compute_checksum(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def archive_document_snapshot(
    document: dict,
    archive_key: str = None,
    include_metadata: bool = True,
    compress: bool = True,
) -> dict:
    s3_client = _get_s3_client()

    if hasattr(document, "to_dict"):
        doc_data = document.to_dict()
    else:
        doc_data = document

    document_id = doc_data.get("document_id", "unknown")
    version = doc_data.get("version", 1)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if archive_key is None:
        archive_key = (
            f"{S3_ARCHIVE_PREFIX}/{document_id}/v{version}/{timestamp}.json.gz"
            if compress
            else f"{S3_ARCHIVE_PREFIX}/{document_id}/v{version}/{timestamp}.json"
        )

    archive_payload = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "document_id": document_id,
        "version": version,
        "document": doc_data,
    }
    if include_metadata:
        archive_payload["archive_metadata"] = {
            "source": "mongodb_atlas",
            "archive_format": "json",
            "compressed": compress,
        }

    json_bytes = json.dumps(archive_payload, indent=2, default=str).encode("utf-8")

    if compress:
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode="wb") as gz:
            gz.write(json_bytes)
        upload_data = buffer.getvalue()
    else:
        upload_data = json_bytes

    checksum = _compute_checksum(upload_data)

    extra_args = {
        "ContentType": "application/gzip" if compress else "application/json",
        "Metadata": {
            "document-id": document_id,
            "document-version": str(version),
            "checksum-sha256": checksum,
        },
    }

    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=archive_key,
        Body=upload_data,
        **extra_args,
    )

    return {
        "document_id": document_id,
        "version": version,
        "archive_key": archive_key,
        "bucket": S3_BUCKET_NAME,
        "checksum": checksum,
        "archived_at": archive_payload["archived_at"],
        "compressed": compress,
    }


def archive_multiple_documents(
    documents: list,
    batch_key: str = None,
    compress: bool = True,
) -> list:
    results = []
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if batch_key is None:
        batch_key = (
            f"{S3_ARCHIVE_PREFIX}/batch/{timestamp}.json.gz"
            if compress
            else f"{S3_ARCHIVE_PREFIX}/batch/{timestamp}.json"
        )

    all_docs = []
    for doc in documents:
        if hasattr(doc, "to_dict"):
            all_docs.append(doc.to_dict())
        else:
            all_docs.append(doc)

    archive_payload = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "batch_count": len(all_docs),
        "documents": all_docs,
        "archive_metadata": {
            "source": "mongodb_atlas",
            "archive_format": "json",
            "compressed": compress,
        },
    }

    json_bytes = json.dumps(archive_payload, indent=2, default=str).encode("utf-8")

    if compress:
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode="wb") as gz:
            gz.write(json_bytes)
        upload_data = buffer.getvalue()
    else:
        upload_data = json_bytes

    checksum = _compute_checksum(upload_data)

    s3_client = _get_s3_client()
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=batch_key,
        Body=upload_data,
        ContentType="application/gzip" if compress else "application/json",
        Metadata={
            "batch-count": str(len(all_docs)),
            "checksum-sha256": checksum,
        },
    )

    for doc in all_docs:
        results.append(
            {
                "document_id": doc.get("document_id", "unknown"),
                "version": doc.get("version", 1),
                "archive_key": batch_key,
                "bucket": S3_BUCKET_NAME,
            }
        )

    return results
