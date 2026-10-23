import os
import boto3
import json
from database_models import Document


def record_export_archive(document: Document, bucket_name: str):
    """
    Exports a document to a JSON file and archives it in an S3 bucket.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    file_name = f"{document.document_id}.json"
    file_content = document.model_dump_json()

    try:
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        return {"status": "success", "file_name": file_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}
