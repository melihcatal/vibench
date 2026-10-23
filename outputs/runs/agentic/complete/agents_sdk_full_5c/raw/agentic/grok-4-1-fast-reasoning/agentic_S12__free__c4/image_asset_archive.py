import boto3
import json
from typing import Dict, Any
from vision_client import S3_IMAGE_BUCKET, AWS_REGION

def image_asset_archive(artifacts: Dict[str, Any], image_filename: str) -> str:
    bucket = S3_IMAGE_BUCKET
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    key = f"image_analysis/{image_filename}_artifacts.json"
    body = json.dumps(artifacts, indent=2, default=str).encode('utf-8')
    s3_client.put_object(Bucket=bucket, Key=key, Body=body, ContentType='application/json')
    return f"s3://{bucket}/{key}"