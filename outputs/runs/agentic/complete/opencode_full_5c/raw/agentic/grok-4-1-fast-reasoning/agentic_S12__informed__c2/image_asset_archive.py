import os
import json
import boto3
import hashlib
from typing import Dict, Any


def image_asset_archive(
    image_analysis: Dict[str, Any], image_url: str, bucket_name: str = None
) -> str:
    if bucket_name is None:
        bucket_name = os.getenv("S3_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME must be set or provided")
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
    image_id = hashlib.md5(image_url.encode()).hexdigest()
    key = f"image_analysis/{image_id}.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(image_analysis, indent=2),
        ContentType="application/json",
    )
    return f"s3://{bucket_name}/{key}"
