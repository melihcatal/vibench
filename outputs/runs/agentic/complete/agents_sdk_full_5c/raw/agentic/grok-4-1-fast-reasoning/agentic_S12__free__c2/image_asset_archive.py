import json
from typing import Dict, Any
from vision_client import s3_client
import boto3

def image_asset_archive(artifacts: Dict[str, Any], bucket: str, key: str) -> str:
    body = json.dumps(artifacts, indent=2).encode('utf-8')
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType='application/json'
    )
    return f"s3://{bucket}/{key}"
