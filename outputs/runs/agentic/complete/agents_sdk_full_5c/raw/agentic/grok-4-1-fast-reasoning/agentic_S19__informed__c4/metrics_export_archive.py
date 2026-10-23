import json
import boto3
from typing import Any

def metrics_export_archive(snapshot: dict[str, Any], bucket: str, key: str) -> None:
    """Archive exported metric snapshots in Amazon S3."""
    s3_client = boto3.client('s3')
    body = json.dumps(snapshot, default=str, indent=2).encode('utf-8')
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType='application/json'
    )