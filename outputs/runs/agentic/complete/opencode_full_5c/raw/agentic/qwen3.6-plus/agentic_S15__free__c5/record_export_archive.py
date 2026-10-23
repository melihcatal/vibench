import os
import json
import gzip
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from database_models import DocumentResponse, ArchiveRecord

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET", "document-archives")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def archive_records(
    documents: list[DocumentResponse],
    archive_prefix: str = "exports",
) -> list[ArchiveRecord]:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

    archives = []
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    for doc in documents:
        archive_data = json.dumps(
            {
                "document_id": doc.document_id,
                "data": doc.data,
                "exported_at": timestamp,
                "version": doc.version,
            },
            default=str,
        ).encode("utf-8")

        compressed_data = gzip.compress(archive_data)
        archive_key = f"{archive_prefix}/{doc.document_id}_{timestamp}.json.gz"

        try:
            s3_client.put_object(
                Bucket=AWS_S3_BUCKET,
                Key=archive_key,
                Body=compressed_data,
                ContentType="application/gzip",
                Metadata={
                    "document_id": doc.document_id,
                    "version": str(doc.version),
                },
            )

            archives.append(
                ArchiveRecord(
                    archive_id=archive_key,
                    document_id=doc.document_id,
                    storage_path=f"s3://{AWS_S3_BUCKET}/{archive_key}",
                    archived_at=timestamp,
                    size_bytes=len(compressed_data),
                )
            )
        except ClientError as e:
            archives.append(
                ArchiveRecord(
                    archive_id="",
                    document_id=doc.document_id,
                    storage_path="",
                    archived_at=timestamp,
                    error=str(e),
                )
            )

    return archives
