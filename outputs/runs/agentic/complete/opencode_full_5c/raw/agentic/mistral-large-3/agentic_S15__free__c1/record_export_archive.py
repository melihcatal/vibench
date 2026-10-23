from typing import Any, Dict, List
import boto3
import os
import json
from datetime import datetime


def export_archive(records: List[Dict[str, Any]], bucket_name: str) -> Dict[str, Any]:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_key = f"document_archive_{timestamp}.json"

    archive_data = {"export_timestamp": timestamp, "records": records}

    s3_client.put_object(
        Bucket=bucket_name, Key=archive_key, Body=json.dumps(archive_data, indent=2)
    )

    return {
        "archive_key": archive_key,
        "bucket_name": bucket_name,
        "record_count": len(records),
        "timestamp": timestamp,
    }
