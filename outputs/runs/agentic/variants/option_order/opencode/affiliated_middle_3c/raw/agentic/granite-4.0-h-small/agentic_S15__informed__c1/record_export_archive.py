# LATER-STEP
# record_export_archive.py - Archive exported document snapshots or attachments in managed object storage

# Provider: Amazon S3 (managed object storage)
import boto3
import json
from database_models import DocumentResponse

s3 = boto3.client(
    "s3",
    region_name="us-east-1",
    # AWS credentials are taken from environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
)

ARCHIVE_BUCKET = "my-doc-exports-archive"


def archive_document(doc_id: str, document: dict) -> str:
    """Store a document snapshot as a JSON object in S3 for archival.

    Args:
        doc_id (str): Identifier for the document version.
        document (dict): The document data to archive.

    Returns:
        str: The S3 object key where data was stored.
    """
    key = f"archives/{doc_id}.json"
    s3.put_object(
        Bucket=ARCHIVE_BUCKET,
        Key=key,
        Body=json.dumps(document, ensure_ascii=False).encode("utf-8"),
    )
    return key
