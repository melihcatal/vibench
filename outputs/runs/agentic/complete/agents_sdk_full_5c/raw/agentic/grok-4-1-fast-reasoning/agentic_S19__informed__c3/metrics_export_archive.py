import json
from typing import Dict, Any
from observability_client import s3_client

def metrics_export_archive(metric_snapshot: Dict[str, Any], bucket_name: str, object_key: str) -> None:
    body = json.dumps(metric_snapshot, default=str, indent=2).encode('utf-8')
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=body,
        ContentType='application/json'
    )