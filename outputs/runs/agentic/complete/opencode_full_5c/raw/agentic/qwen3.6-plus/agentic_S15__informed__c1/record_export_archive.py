import os
import json
import datetime
import boto3
from botocore.exceptions import ClientError
from database_models import DocumentResponse, serialize_for_storage


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "document-archive")


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def archive_documents(
    documents: list[DocumentResponse],
    archive_prefix: str = "document-snapshots",
) -> list[dict]:
    s3_client = get_s3_client()
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    results = []
    for doc in documents:
        serialized = serialize_for_storage(doc)
        payload = json.dumps(serialized, default=str, indent=2)
        object_key = (
            f"{archive_prefix}/{doc.collection}/{doc.document_id}_{timestamp}.json"
        )
        try:
            s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=object_key,
                Body=payload.encode("utf-8"),
                ContentType="application/json",
            )
            results.append(
                {
                    "document_id": doc.document_id,
                    "collection": doc.collection,
                    "s3_bucket": S3_BUCKET_NAME,
                    "s3_key": object_key,
                    "archived_at": timestamp,
                    "status": "success",
                }
            )
        except ClientError as e:
            results.append(
                {
                    "document_id": doc.document_id,
                    "collection": doc.collection,
                    "s3_bucket": S3_BUCKET_NAME,
                    "s3_key": object_key,
                    "archived_at": timestamp,
                    "status": "failed",
                    "error": str(e),
                }
            )
    return results
