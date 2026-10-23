import json
import os
from typing import Dict

import boto3


S3_BUCKET = os.environ.get("IMAGE_ASSET_ARCHIVE_BUCKET", "")
S3_PREFIX = os.environ.get("IMAGE_ASSET_ARCHIVE_PREFIX", "image-analysis/")


def archive_image_artifacts(asset_name: str, metadata: Dict) -> str:
    if not S3_BUCKET:
        raise ValueError("IMAGE_ASSET_ARCHIVE_BUCKET is required")
    s3 = boto3.client("s3")
    key = f"{S3_PREFIX.rstrip('/')}/{asset_name}.json"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=json.dumps(metadata).encode("utf-8"), ContentType="application/json")
    return f"s3://{S3_BUCKET}/{key}"
