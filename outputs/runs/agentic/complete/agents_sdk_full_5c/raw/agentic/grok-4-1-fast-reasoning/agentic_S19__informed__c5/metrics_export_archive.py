import boto3
import json
from io import BytesIO
from typing import Any

def archive_metrics_export(
    data: Dict[str, Any],
    bucket_name: str,
    object_key: str
):
    client = boto3.client('s3')
    body = BytesIO(json.dumps(data, indent=2).encode('utf-8'))
    client.upload_fileobj(Fileobj=body, Bucket=bucket_name, Key=object_key)
