import os
import json
from typing import Dict, Any
import boto3
from database_models import Document

def record_export_archive(document: Document, export_format: str = "json") -> Dict[str, Any]:
    """
    Archives an exported document snapshot in AWS S3 object storage.
    The document is serialized to a specified format (e.g., JSON) before archiving.
    """
    s3_bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
    if not s3_bucket_name:
        raise ValueError("AWS_S3_BUCKET_NAME environment variable not set.")
    
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    s3 = boto3.client(
        "s3",
        region_name=region_name,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    file_content: bytes
    content_type: str
    file_key: str

    if export_format == "json":
        file_content = json.dumps(document.model_dump(), indent=2).encode('utf-8')
        content_type = "application/json"
        file_key = f"documents/{document.id}.json"
    else:
        file_content = json.dumps(document.model_dump(), indent=2).encode('utf-8')
        content_type = "application/json"
        file_key = f"documents/{document.id}.json"

    try:
        s3.put_object(
            Bucket=s3_bucket_name,
            Key=file_key,
            Body=file_content,
            ContentType=content_type
        )
        return {
            "status": "success",
            "bucket": s3_bucket_name,
            "key": file_key,
            "url": f"s3://{s3_bucket_name}/{file_key}"
        }
    except Exception as e:
        print(f"Error archiving document to S3: {e}")
        raise
