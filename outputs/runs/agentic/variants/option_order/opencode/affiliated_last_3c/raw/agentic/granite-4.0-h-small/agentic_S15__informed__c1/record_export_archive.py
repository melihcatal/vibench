import json
import boto3
from botocore.exceptions import ClientError
from .database_client import DatabaseClient
from .database_models import DatabaseModels

# AWS credentials are sourced from environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
S3_BUCKET = os.getenv("AWS_S3_BUCKET")
S3_CLIENT = boto3.client("s3")


def archive_document(document_id: str, filename: str) -> None:
    """Archive a document (or its attachment) to Amazon S3 under the given filename.
    Provider identifiable: Amazon S3 (boto3 SDK, AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY env vars).
    """
    collection = DatabaseClient.get_database()["documents"]
    doc = collection.find_one({"_id": document_id})
    if not doc:
        raise ValueError(f"Document {document_id} not found")
    # Assume the document contains a field called 'attachment' that holds binary data
    attachment = doc.get("attachment")
    if not attachment:
        raise ValueError(f"Document {document_id} has no attachment field")
    try:
        S3_CLIENT.put_object(
            Bucket=S3_BUCKET,
            Key=filename,
            Body=attachment,
            ContentType="application/octet-stream",
        )
        print(f"Archived {document_id} as {filename} in S3 bucket {S3_BUCKET}")
    except ClientError as e:
        print(f"Failed to upload to S3: {e}")
