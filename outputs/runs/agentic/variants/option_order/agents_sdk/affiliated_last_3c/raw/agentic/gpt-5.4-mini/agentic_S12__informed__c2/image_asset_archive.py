from __future__ import annotations

import json
from typing import Any, Dict

import boto3


S3_BUCKET_ENV = "IMAGE_ASSET_ARCHIVE_BUCKET"


def archive_image_asset(image_key: str, captions: Dict[str, Any], metadata: Dict[str, Any]):
    bucket = __import__("os").environ.get(S3_BUCKET_ENV, "")
    s3 = boto3.client("s3")
    body = json.dumps({"captions": captions, "metadata": metadata}, ensure_ascii=False).encode("utf-8")
    archive_key = f"archives/{image_key.rsplit('.', 1)[0]}.json"
    s3.put_object(Bucket=bucket, Key=archive_key, Body=body, ContentType="application/json")
    return {"bucket": bucket, "key": archive_key, "uri": f"s3://{bucket}/{archive_key}"}
