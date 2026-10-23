import os
import boto3
from botocore.exceptions import NoCredentialsError

# MinIO/Amazon S3 configuration via env
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY_ID")
S3_SECRET_KEY = os.getenv("S3_SECRET_ACCESS_KEY")

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)


def archive_document_snapshot(document_id: str, snapshot_bytes: bytes):
    """Store a snapshot of a document as an object in S3/MinIO.

    The object key follows the pattern `snapshots/{document_id}/{timestamp}.json`.
    """
    timestamp = os.getenv("SNAPSHOT_TIMESTAMP") or str(int(os.time()))
    key = f"snapshots/{document_id}/{timestamp}.json"
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=snapshot_bytes,
            ContentType="application/json",
        )
        return {"status": "archived", "key": key}
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not configured for S3/MinIO")
