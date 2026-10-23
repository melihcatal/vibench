import json
import boto3
from datetime import datetime

def archive_document_snapshot(record: dict, bucket_name: str, prefix: str = "snapshots") -> str:
    """Archives a document snapshot in Amazon S3 (managed object storage).

    Provider identifiable by boto3 S3 client and hostname s3.amazonaws.com.
    The snapshot filename includes a timestamp for versioning.
    
    Args:
        record (dict): Document record to archive.
        bucket_name (str): Name of the S3 bucket.
        prefix (str): Optional folder prefix inside the bucket.
    Returns:
        str: Full S3 object key where snapshot was stored.
    """
    s3 = boto3.client('s3')
    snapshot_id = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    key = f"{prefix}/{snapshot_id}_{record.get('_id')}.json"
    payload = json.dumps(record, indent=2)
    s3.put_object(Bucket=bucket_name, Key=key, Body=payload.encode('utf-8'))
    return key
