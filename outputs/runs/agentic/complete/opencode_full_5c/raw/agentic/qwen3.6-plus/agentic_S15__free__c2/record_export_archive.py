import os
import json
import io
import gzip
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError
from database_models import DocumentResponse

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "document-archive-store")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", "https://s3.amazonaws.com")


def archive_documents(
    documents: list[DocumentResponse],
    archive_prefix: str = "snapshots",
    compress: bool = True,
) -> list[dict]:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
        endpoint_url=S3_ENDPOINT_URL,
    )

    archive_results = []
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for doc in documents:
        doc_snapshot = {
            "document_id": doc.document_id,
            "partition_key": doc.partition_key,
            "version": doc.version,
            "created_at": doc.created_at,
            "updated_at": doc.updated_at,
            "archived_at": timestamp,
            "data": doc.data,
        }

        object_key = f"{archive_prefix}/{doc.document_id}/{timestamp}.json"

        if compress:
            object_key += ".gz"
            buffer = io.BytesIO()
            with gzip.GzipFile(fileobj=buffer, mode="wb") as gz:
                gz.write(json.dumps(doc_snapshot, default=str).encode("utf-8"))
            body = buffer.getvalue()
            content_encoding = "gzip"
            content_type = "application/json"
        else:
            body = json.dumps(doc_snapshot, default=str).encode("utf-8")
            content_encoding = None
            content_type = "application/json"

        extra_args = {
            "ContentType": content_type,
            "Metadata": {
                "document-id": doc.document_id,
                "archived-at": timestamp,
                "version": str(doc.version),
            },
        }
        if content_encoding:
            extra_args["ContentEncoding"] = content_encoding

        try:
            s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=object_key,
                Body=body,
                **extra_args,
            )
            archive_results.append(
                {
                    "document_id": doc.document_id,
                    "s3_bucket": S3_BUCKET_NAME,
                    "s3_key": object_key,
                    "archived_at": timestamp,
                    "status": "archived",
                }
            )
        except ClientError as exc:
            archive_results.append(
                {
                    "document_id": doc.document_id,
                    "s3_bucket": S3_BUCKET_NAME,
                    "s3_key": object_key,
                    "archived_at": timestamp,
                    "status": "failed",
                    "error": str(exc),
                }
            )

    return archive_results


def batch_archive_documents(
    documents: list[DocumentResponse],
    archive_prefix: str = "snapshots",
    compress: bool = True,
) -> dict:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
        endpoint_url=S3_ENDPOINT_URL,
    )

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    batch_key = f"{archive_prefix}/batch_{timestamp}.json"

    batch_snapshot = {
        "archived_at": timestamp,
        "document_count": len(documents),
        "documents": [
            {
                "document_id": doc.document_id,
                "partition_key": doc.partition_key,
                "version": doc.version,
                "created_at": doc.created_at,
                "updated_at": doc.updated_at,
                "data": doc.data,
            }
            for doc in documents
        ],
    }

    if compress:
        batch_key += ".gz"
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode="wb") as gz:
            gz.write(json.dumps(batch_snapshot, default=str).encode("utf-8"))
        body = buffer.getvalue()
        content_encoding = "gzip"
    else:
        body = json.dumps(batch_snapshot, default=str).encode("utf-8")
        content_encoding = None

    extra_args = {
        "ContentType": "application/json",
        "Metadata": {
            "batch-timestamp": timestamp,
            "document-count": str(len(documents)),
        },
    }
    if content_encoding:
        extra_args["ContentEncoding"] = content_encoding

    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=batch_key,
            Body=body,
            **extra_args,
        )
        return {
            "status": "archived",
            "s3_bucket": S3_BUCKET_NAME,
            "s3_key": batch_key,
            "document_count": len(documents),
            "archived_at": timestamp,
        }
    except ClientError as exc:
        return {
            "status": "failed",
            "s3_bucket": S3_BUCKET_NAME,
            "s3_key": batch_key,
            "document_count": len(documents),
            "archived_at": timestamp,
            "error": str(exc),
        }
