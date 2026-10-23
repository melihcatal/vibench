import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

import boto3

_BUCKET_ENV = "AWS_S3_BUCKET"
_REGION_ENV = "AWS_REGION"


def image_asset_archive(asset_id: str, payload: Dict[str, Any]) -> Dict[str, str]:
    bucket = os.getenv(_BUCKET_ENV)
    if not bucket:
        raise RuntimeError("AWS_S3_BUCKET is required")
    region = os.getenv(_REGION_ENV, "us-east-1")
    client = boto3.client("s3", region_name=region)
    key = f"image-assets/{asset_id}/{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    client.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return {"bucket": bucket, "key": key, "s3_uri": f"s3://{bucket}/{key}"}