import os
import boto3
from botocore.exceptions import ClientError
from typing import Dict

# Provider identification – object storage (Amazon S3) in this example
storage_provider = "s3"

S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1",
)


def archive_document_snapshot(
    snapshot_id: str, document: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Store a JSON snapshot of a document (or its attachment metadata) in S3.
    Generates a deterministic key using the snapshot_id and stores the JSON.
    Returns a dict with the S3 key and a success flag.
    """
    key = f"snapshots/{snapshot_id}.json"
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=json.dumps(document).encode("utf-8"),
            ContentType="application/json",
        )
        return {"snapshot_id": snapshot_id, "s3_key": key, "stored": True}
    except ClientError as e:
        return {"snapshot_id": snapshot_id, "error": str(e), "stored": False}
