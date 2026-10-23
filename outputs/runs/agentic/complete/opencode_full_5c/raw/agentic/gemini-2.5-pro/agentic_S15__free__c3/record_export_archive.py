import os
import boto3
from botocore.exceptions import ClientError
import json
from database_models import Document


def archive_document_to_s3(document: Document):
    """
    Archives a document snapshot as a JSON file in an S3 bucket.
    """
    s3_client = boto3.client("s3")
    bucket_name = os.environ.get("S3_BUCKET_NAME")

    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME environment variable not set.")

    document_id = document.get("document_id")
    if not document_id:
        raise ValueError("Document must have a 'document_id'.")

    file_name = f"{document_id}.json"

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"archives/{file_name}",
            Body=json.dumps(document, indent=4),
            ContentType="application/json",
        )
        return {
            "status": "success",
            "bucket": bucket_name,
            "key": f"archives/{file_name}",
        }
    except ClientError as e:
        return {"status": "error", "message": e.response["Error"]["Message"]}
