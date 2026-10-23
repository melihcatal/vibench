import json
import uuid
import boto3
from database_models import DatabaseModels

# Amazon S3 (managed object storage) is used as the concrete provider for archiving


def record_export_archive(
    record_id: str, snapshot: dict, bucket_name: str = "my-export-bucket"
) -> str:
    """Archive a document snapshot (or its attachments) to S3 and return the object key.","""
    # Normalize snapshot to JSON string
    payload = DatabaseModels.firestore_snapshot_to_response(snapshot)
    json_body = json.dumps(payload, ensure_ascii=False, indent=2)
    s3 = boto3.client("s3")
    # Use a deterministic key based on record_id; you could also add timestamps or prefixes
    object_key = f"archives/{record_id}.json"
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=json_body)
    return object_key
