import os
import json
import boto3
from typing import List
from botocore.exceptions import NoCredentialsError, ClientError

s3_client = boto3.client("s3")

def archive_document_snapshots(bucket_name: str, key_prefix: str, documents: List[dict]) -> bool:
    snapshot_data = {
        "exported_at": os.getenv("EXPORT_TIMESTAMP", "unknown"),
        "count": len(documents),
        "documents": documents
    }
    body = json.dumps(snapshot_data, indent=2).encode("utf-8")
    object_key = f"{key_prefix}/{os.urandom(16).hex()}.json"
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=body,
            ContentType="application/json"
        )
        return True
    except (NoCredentialsError, ClientError):
        return False