import os
import json
import gzip
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from database_models import FetchResponse, QueryResponse


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "document-store-archives")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=S3_REGION,
    )


def archive_document_snapshot(
    document_id: str,
    document_data: dict,
    metadata: dict | None = None,
    compress: bool = True,
) -> dict:
    s3_client = get_s3_client()

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    archive_key = f"archives/{document_id}/{timestamp}.json"

    if compress:
        archive_key += ".gz"

    snapshot = {
        "document_id": document_id,
        "archived_at": timestamp,
        "metadata": metadata or {},
        "data": document_data,
    }

    if compress:
        content = gzip.compress(json.dumps(snapshot, default=str).encode("utf-8"))
        content_type = "application/gzip"
    else:
        content = json.dumps(snapshot, default=str).encode("utf-8")
        content_type = "application/json"

    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=archive_key,
            Body=content,
            ContentType=content_type,
            Metadata={
                "document-id": document_id,
                "archived-at": timestamp,
                "compressed": str(compress).lower(),
            },
        )

        return {
            "provider": "amazon_s3",
            "bucket": S3_BUCKET_NAME,
            "key": archive_key,
            "document_id": document_id,
            "archived_at": timestamp,
            "compressed": compress,
            "size_bytes": len(content),
            "status": "archived",
        }
    except ClientError as e:
        return {
            "provider": "amazon_s3",
            "bucket": S3_BUCKET_NAME,
            "key": archive_key,
            "document_id": document_id,
            "status": "error",
            "error": str(e),
        }


def archive_fetch_response(
    fetch_response: FetchResponse, metadata: dict | None = None, compress: bool = True
) -> dict:
    if not fetch_response.found or not fetch_response.data:
        return {
            "provider": "amazon_s3",
            "status": "skipped",
            "message": "No document data to archive",
        }
    return archive_document_snapshot(
        fetch_response.document_id, fetch_response.data, metadata, compress
    )


def archive_query_results(
    query_response: QueryResponse, metadata: dict | None = None, compress: bool = True
) -> dict:
    s3_client = get_s3_client()

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    archive_key = (
        f"archives/batch/{query_response.field}_{query_response.value}/{timestamp}.json"
    )

    if compress:
        archive_key += ".gz"

    batch_snapshot = {
        "archived_at": timestamp,
        "query_field": query_response.field,
        "query_value": query_response.value,
        "partition_key": query_response.partition_key,
        "total_count": query_response.total_count,
        "metadata": metadata or {},
        "records": [item.data for item in query_response.items],
    }

    if compress:
        content = gzip.compress(json.dumps(batch_snapshot, default=str).encode("utf-8"))
        content_type = "application/gzip"
    else:
        content = json.dumps(batch_snapshot, default=str).encode("utf-8")
        content_type = "application/json"

    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=archive_key,
            Body=content,
            ContentType=content_type,
            Metadata={
                "query-field": query_response.field,
                "query-value": query_response.value,
                "record-count": str(query_response.total_count),
                "archived-at": timestamp,
            },
        )

        return {
            "provider": "amazon_s3",
            "bucket": S3_BUCKET_NAME,
            "key": archive_key,
            "archived_at": timestamp,
            "record_count": query_response.total_count,
            "compressed": compress,
            "size_bytes": len(content),
            "status": "archived",
        }
    except ClientError as e:
        return {
            "provider": "amazon_s3",
            "bucket": S3_BUCKET_NAME,
            "key": archive_key,
            "status": "error",
            "error": str(e),
        }


if __name__ == "__main__":
    sample_data = {
        "title": "Archived Document",
        "content": "This document has been archived to S3.",
        "status": "archived",
    }
    result = archive_document_snapshot("doc-001", sample_data)
    print(result)
