import os
from typing import Any, Dict

import boto3

from vision_models import VisionResult


def image_asset_archive(bucket: str, key: str, payload: Dict[str, Any]) -> VisionResult:
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    body = str(payload).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return VisionResult(provider="aws.s3", kind="archive", source=bucket, data={"key": key, "bytes": len(body)})
