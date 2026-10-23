import boto3
import os
import json
from typing import Dict, Any
from database_models import Document

def record_export_archive(document: Document, bucket_name: str, folder_prefix: str = "documents/") -> Dict[str, Any]:
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    s3 = boto3.client("s3", region_name=aws_region)

    # Construct the object key (path in S3)
    object_key = f"{folder_prefix}{document.id}.json"

    # Convert the document to a JSON string
    document_json = json.dumps(document.to_item(), indent=2)

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=document_json,
            ContentType="application/json"
        )
        return {
            "status": "archived",
            "bucket_name": bucket_name,
            "object_key": object_key,
            "message": f"Document {document.id} archived successfully to s3://{bucket_name}/{object_key}"
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": f"Failed to archive document {document.id}: {str(e)}"
        }
