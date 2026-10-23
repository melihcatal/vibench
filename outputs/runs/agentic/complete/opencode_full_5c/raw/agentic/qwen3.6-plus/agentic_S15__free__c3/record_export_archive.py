import os
import io
import json
import gzip
from datetime import datetime
from typing import List, Optional
import boto3
from botocore.exceptions import ClientError
from database_models import DocumentResponse, ArchiveRecord


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "nosql-document-archives")


def archive_documents_to_s3(
    documents: List[DocumentResponse],
    archive_prefix: Optional[str] = None,
    compress: bool = True,
) -> ArchiveRecord:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    if archive_prefix is None:
        archive_prefix = "archives"
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    archive_filename = f"{archive_prefix}/snapshot_{timestamp}.json"
    if compress:
        archive_filename += ".gz"
    export_data = {
        "exported_at": timestamp,
        "total_documents": len(documents),
        "documents": [],
    }
    for doc in documents:
        export_data["documents"].append(
            {
                "document_id": doc.document_id,
                "collection": doc.collection,
                "version": doc.version,
                "created_at": doc.created_at,
                "updated_at": doc.updated_at,
                "data": doc.data,
                "metadata": doc.metadata,
            }
        )
    json_bytes = json.dumps(export_data, indent=2, default=str).encode("utf-8")
    if compress:
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
            gz.write(json_bytes)
        upload_data = buf.getvalue()
    else:
        upload_data = json_bytes
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=archive_filename,
            Body=upload_data,
            ContentType="application/json" if not compress else "application/gzip",
            Metadata={
                "export-timestamp": timestamp,
                "document-count": str(len(documents)),
                "compressed": str(compress).lower(),
            },
        )
    except ClientError as exc:
        raise RuntimeError(
            f"Failed to upload archive to S3 bucket {S3_BUCKET_NAME}: {exc}"
        ) from exc
    document_ids = [doc.document_id for doc in documents]
    return ArchiveRecord(
        archive_id=archive_filename,
        source_collection=documents[0].collection if documents else "unknown",
        document_ids=document_ids,
        storage_key=f"s3://{S3_BUCKET_NAME}/{archive_filename}",
        archived_at=timestamp,
        size_bytes=len(upload_data),
    )


if __name__ == "__main__":
    sample_docs = [
        DocumentResponse(
            document_id="user_001",
            data={"name": "Alice", "email": "alice@example.com"},
            collection="users",
            version=2,
        ),
    ]
    archive = archive_documents_to_s3(sample_docs, archive_prefix="users/export")
    print(archive)
