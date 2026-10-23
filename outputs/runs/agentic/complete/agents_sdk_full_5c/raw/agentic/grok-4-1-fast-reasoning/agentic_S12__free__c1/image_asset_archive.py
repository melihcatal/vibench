import boto3
import os
import json
from typing import Dict, Any

def image_asset_archive(artifacts: Dict[str, Any], bucket_name: str, object_key: str) -> str:
    s3_client = boto3.client('s3', region_name='us-east-1')
    json_str = json.dumps(artifacts, indent=2)
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json_str,
        ContentType='application/json'
    )
    return f"s3://{bucket_name}/{object_key}"