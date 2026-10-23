import boto3
import json
import time
import os
from database_models import Documents


def archive_exported_document_snapshots_or_attachments(
    records: Documents, bucket_name: str
) -> list[str]:
    s3_client = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
    uploaded_keys = []
    for idx, record in enumerate(records):
        doc_id = record.get("id", f"unknown_{idx}")
        timestamp = int(time.time())
        key = f"archives/{doc_id}_{timestamp}.json"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(record, default=str),
            ContentType="application/json",
        )
        uploaded_keys.append(key)
    return uploaded_keys
