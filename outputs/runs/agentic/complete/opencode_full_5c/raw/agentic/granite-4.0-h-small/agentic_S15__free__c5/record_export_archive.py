# record_export_archive.py
# Later-step: Archive exported document snapshots/attachments in managed object storage
import os
import json
from boto3 import client
from database_client import get_dynamodb_client


def archive_document_snapshot(document_id: str, snapshot_data: dict) -> None:
    """Store a snapshot of a document as an object in S3 (managed object storage).

    Args:
        document_id (str): Identifier of the related document.
        snapshot_data (dict): JSON-serializable snapshot content.
    """
    s3 = client("s3")
    bucket_name = os.getenv("ARCHIVE_BUCKET", "doc-archive")
    key = f"snapshots/{document_id}.json"
    # Store JSON as UTF-8 text
    s3.put_object(
        Bucket=bucket_name, Key=key, Body=json.dumps(snapshot_data).encode("utf-8")
    )
