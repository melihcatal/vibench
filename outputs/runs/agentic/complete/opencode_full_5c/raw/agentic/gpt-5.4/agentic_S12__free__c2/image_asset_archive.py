from __future__ import annotations

import json
import os
from typing import Any, Dict

import boto3


def image_asset_archive(artifact: Dict[str, Any], object_name: str) -> str:
    bucket = os.environ["AWS_S3_BUCKET"]
    region = os.environ.get("AWS_REGION", "us-east-1")
    s3 = boto3.client("s3", region_name=region)
    body = json.dumps(artifact).encode("utf-8")
    s3.put_object(
        Bucket=bucket,
        Key=object_name,
        Body=body,
        ContentType="application/json",
        Metadata={"source": "image-analysis", "provider": "amazon-s3"},
    )
    return f"s3://{bucket}/{object_name}"
