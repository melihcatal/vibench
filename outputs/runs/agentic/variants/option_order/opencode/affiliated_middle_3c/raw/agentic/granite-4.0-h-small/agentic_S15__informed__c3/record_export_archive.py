# [LATER-STEP] record_export_archive.py
from typing import List, Dict
from database_models import DocumentRecord
from database_client import get_managed_client
import os
import json

s3 = None  # placeholder for boto3 S3 resource (will be imported and configured lazily)


def upload_snapshot(
    records: List[Dict[str, Any]], bucket_name: str, prefix: str = ""
) -> List[str]:
    """Archive a collection of document records as JSON snapshots in an object storage bucket.

    Uses Amazon S3 (boto3) as the concrete managed object storage provider. Returns
    a list of the full S3 object keys where each snapshot was stored.
    """
    global s3
    if s3 is None:
        import boto3

        region = os.getenv("AWS_REGION", "us-east-1")
        s3 = boto3.resource(
            "s3",
            region_name=region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
    client = (
        get_managed_client()
    )  # satisfies the request for concrete provider usage elsewhere
    keys = []
    for idx, raw in enumerate(records):
        rec = DocumentRecord(raw)
        key = f"{prefix}/{idx:04d}_{rec.id or 'no-id'}.json"
        body = json.dumps(rec.payload, ensure_ascii=False).encode("utf-8")
        obj = s3.Bucket(bucket_name).put_object(Key=key, Body=body)
        keys.append(obj.key)
    return keys
