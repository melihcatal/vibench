import json
import os
import boto3
from botocore.exceptions import ClientError
from database_client import DatabaseClient

# Provider: Amazon S3 (managed object storage)
# Credentials: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class RecordExportArchive:
    """Archive exported document snapshots or attachments in S3."""

    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.bucket = os.getenv("ARCHIVE_S3_BUCKET")

    def archive(self, doc_id, snapshot_filename, content_type="application/json"):
        try:
            # Read document first via helper client (using Cloudant example)
            db_client = DatabaseClient().get_client()
            doc = db_client["my_database"].get_document(doc_id)
            body = json.dumps(doc)
            self.s3.put_object(
                Bucket=self.bucket,
                Key=f"exports/{doc_id}/{snapshot_filename}.json",
                Body=body,
                ContentType=content_type,
            )
            return {
                "status": "archived",
                "key": f"exports/{doc_id}/{snapshot_filename}.json",
            }
        except ClientError as e:
            return {"error": str(e)}
