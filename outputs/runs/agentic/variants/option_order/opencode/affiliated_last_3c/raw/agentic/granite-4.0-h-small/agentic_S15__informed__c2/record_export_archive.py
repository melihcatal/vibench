import os
import boto3
from database_client import get_dynamodb_client
from database_models import DocumentFetchResponse
from pathlib import Path

s3 = boto3.client("s3")


class RecordExportArchive:
    @staticmethod
    def archive(
        response: DocumentFetchResponse, bucket_name: str, prefix: str = "export/"
    ) -> str:
        """Archive a fetched document as a JSON file in Amazon S3.

        The document is stored under the supplied bucket and optional prefix. A unique
        object key (UUID) is generated to avoid collisions.
        """
        if not response.found:
            raise ValueError("Cannot archive: no document found")
        doc = response.document
        # Generate a unique object key
        object_key = f"{prefix}{os.urandom(16).hex()}.json"
        # Serialize document to JSON (ensure ASCII safe)
        payload = json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=payload)
        return f"https://{bucket_name}.s3.{os.getenv('AWS_REGION', 'us-east-1')}.amazonaws.com/{object_key}"
