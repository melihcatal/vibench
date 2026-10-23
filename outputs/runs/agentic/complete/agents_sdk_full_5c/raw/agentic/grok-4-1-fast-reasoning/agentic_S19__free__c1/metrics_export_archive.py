import boto3
import os
import json
from datetime import datetime
from typing import Dict, Any
from observability_client import get_s3_archive_bucket

def archive_exported_metric_snapshots(snapshot_data: Dict[str, Any], key_prefix: str = "metrics/archives/") -> str:
    bucket = get_s3_archive_bucket()
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    key = f"{key_prefix}{timestamp}.json"
    client = boto3.client('s3', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(snapshot_data, default=str, indent=2),
        ContentType='application/json'
    )
    return f"s3://{bucket}/{key}"
