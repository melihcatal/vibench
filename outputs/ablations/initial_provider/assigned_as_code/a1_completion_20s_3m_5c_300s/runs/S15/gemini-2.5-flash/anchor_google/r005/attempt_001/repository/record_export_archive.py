import os
import json
import boto3
from typing import Dict, Any


def record_export_archive(document_data: Dict[str, Any], bucket_name: str, object_key: str) -> Dict[str, Any]:
    # Initialize S3 client
    s3_client = boto3.client("s3")

    # Convert document data to JSON string
    document_json = json.dumps(document_data, indent=2)

    try:
        # Upload the JSON string to S3
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=document_json, ContentType="application/json")
        return {"status": "success", "bucket": bucket_name, "key": object_key}
    except Exception as e:
        return {"status": "error", "message": str(e)}
