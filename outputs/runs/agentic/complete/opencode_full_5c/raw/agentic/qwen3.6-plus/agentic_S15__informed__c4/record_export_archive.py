import io
import json
import os
import datetime
import gzip
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from database_models import DocumentResponse


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "document-archive")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")


def export_archive_documents(
    documents: List[Dict[str, Any]],
    archive_prefix: Optional[str] = None,
    compress: bool = True,
    include_metadata: bool = True,
) -> DocumentResponse:
    if not documents:
        return DocumentResponse(
            success=False,
            error="No documents provided for archival",
        )

    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        return DocumentResponse(
            success=False,
            error="AWS credentials not configured",
        )

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=S3_REGION,
    )

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    archive_prefix = archive_prefix or "document-archives"

    archive_data = {
        "exported_at": timestamp,
        "document_count": len(documents),
        "documents": [],
    }

    for doc in documents:
        doc_entry = {
            "id": doc.get("id", doc.get("_id", "unknown")),
            "data": {k: v for k, v in doc.items() if k not in ("_id", "id")},
        }
        if include_metadata:
            doc_entry["metadata"] = {
                "created_at": doc.get("created_at"),
                "updated_at": doc.get("updated_at"),
                "partition_key": doc.get("partition_key"),
                "version": doc.get("version"),
            }
        archive_data["documents"].append(doc_entry)

    json_content = json.dumps(archive_data, indent=2, default=str)

    if compress:
        file_extension = "json.gz"
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode="wb") as gz:
            gz.write(json_content.encode("utf-8"))
        file_content = buffer.getvalue()
        content_type = "application/gzip"
    else:
        file_extension = "json"
        file_content = json_content.encode("utf-8")
        content_type = "application/json"

    object_key = f"{archive_prefix}/archive-{timestamp}.{file_extension}"

    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=object_key,
            Body=file_content,
            ContentType=content_type,
            Metadata={
                "document-count": str(len(documents)),
                "exported-at": timestamp,
                "compressed": str(compress),
            },
        )

        archive_url = f"s3://{S3_BUCKET_NAME}/{object_key}"

        return DocumentResponse(
            success=True,
            document={
                "archive_key": object_key,
                "archive_url": archive_url,
                "bucket": S3_BUCKET_NAME,
                "document_count": len(documents),
                "compressed": compress,
                "exported_at": timestamp,
                "service": "Amazon S3",
            },
        )
    except ClientError as exc:
        return DocumentResponse(
            success=False,
            error=f"S3 archival error: {exc}",
        )
    except Exception as exc:
        return DocumentResponse(
            success=False,
            error=f"Export archive error: {exc}",
        )
