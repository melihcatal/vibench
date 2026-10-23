import boto3
import json
from typing import Any, Dict

def archive_metrics_snapshot(
    snapshot_data: Dict[str, Any],
    bucket_name: str,
    object_key: str,
    region: str = None
):
    client = boto3.client('s3', region_name=region)
    body = json.dumps(snapshot_data, default=str).encode('utf-8')
    client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=body,
        ContentType='application/json'
    )
