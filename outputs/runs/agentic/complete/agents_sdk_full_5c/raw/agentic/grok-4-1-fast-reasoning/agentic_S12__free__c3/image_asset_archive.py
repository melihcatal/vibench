import boto3
import json
import os
from typing import Any, Dict

def image_asset_archive(artifacts: Dict[str, Any], image_path: str, bucket_name: str = None, key_prefix: str = "image_analysis") -> str:
    if bucket_name is None:
        bucket_name = os.getenv("S3_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable required or provide bucket_name parameter")
    s3 = boto3.client("s3")
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    object_key = f"{key_prefix}/{image_name}_artifacts.json"
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(artifacts, indent=2),
        ContentType="application/json"
    )
    return f"s3://{bucket_name}/{object_key}"