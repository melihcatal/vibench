from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError
from database_models import DocumentResponse

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "document-archive-bucket")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")


def archive_documents(
    documents: list[DocumentResponse],
    archive_prefix: str = "document-snapshots",
    bucket: str | None = None,
) -> list[dict[str, Any]]:
    bucket_name = bucket or S3_BUCKET_NAME

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=S3_REGION,
    )

    archived = []

    for doc in documents:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        object_key = f"{archive_prefix}/{doc.document_id}/{timestamp}.json"

        snapshot = {
            "document_id": doc.document_id,
            "data": doc.data,
            "partition_key": doc.partition_key,
            "version": doc.version,
            "archived_at": timestamp,
            "source": "managed_nosql_store",
        }

        try:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=json.dumps(snapshot, default=str),
                ContentType="application/json",
            )

            archived.append(
                {
                    "document_id": doc.document_id,
                    "s3_key": object_key,
                    "bucket": bucket_name,
                    "status": "archived",
                }
            )
        except ClientError as e:
            archived.append(
                {
                    "document_id": doc.document_id,
                    "s3_key": object_key,
                    "bucket": bucket_name,
                    "status": "failed",
                    "error": str(e),
                }
            )

    return archived
