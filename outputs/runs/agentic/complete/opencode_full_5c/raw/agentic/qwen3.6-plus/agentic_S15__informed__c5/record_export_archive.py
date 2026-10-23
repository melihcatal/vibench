import os
import json
import io
import gzip
from datetime import datetime, timezone
import boto3
from botocore.config import Config
from database_models import DocumentResponse


def get_s3_client():
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    endpoint_url = os.environ.get("S3_ENDPOINT_URL")

    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        signature_version="s3v4",
    )

    kwargs = {
        "region_name": region,
        "config": config,
    }
    if aws_access_key_id and aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url

    return boto3.client("s3", **kwargs)


def archive_documents_to_s3(documents, bucket_name=None, prefix=None, compress=True):
    bucket_name = bucket_name or os.environ.get(
        "S3_ARCHIVE_BUCKET", "document-archives"
    )
    prefix = prefix or os.environ.get("S3_ARCHIVE_PREFIX", "document-snapshots")

    s3_client = get_s3_client()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive_key = f"{prefix}/{timestamp}/documents.json"

    doc_list = []
    for doc in documents:
        if isinstance(doc, DocumentResponse):
            doc_list.append(
                {
                    "document_id": doc.document_id,
                    "data": doc.data,
                    "metadata": doc.metadata,
                    "version": doc.version,
                }
            )
        elif isinstance(doc, dict):
            doc_list.append(doc)

    json_bytes = json.dumps(doc_list, indent=2, default=str).encode("utf-8")

    if compress:
        archive_key += ".gz"
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
            gz.write(json_bytes)
        upload_data = buf.getvalue()
    else:
        upload_data = json_bytes

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=archive_key,
            Body=upload_data,
            ContentType="application/json" if not compress else "application/gzip",
            Metadata={
                "document-count": str(len(doc_list)),
                "archived-at": timestamp,
            },
        )

        return {
            "success": True,
            "bucket": bucket_name,
            "key": archive_key,
            "document_count": len(doc_list),
            "compressed": compress,
            "size_bytes": len(upload_data),
        }
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "bucket": bucket_name,
            "key": archive_key,
        }


def archive_single_document_to_s3(
    document, bucket_name=None, prefix=None, compress=True
):
    return archive_documents_to_s3([document], bucket_name, prefix, compress)
