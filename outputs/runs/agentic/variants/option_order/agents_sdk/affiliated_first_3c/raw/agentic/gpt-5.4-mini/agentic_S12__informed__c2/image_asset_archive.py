from __future__ import annotations

import json
import os
from typing import Any, Dict

import boto3


def image_asset_archive(bucket: str, key: str, artifact: Dict[str, Any]) -> str:
    s3 = boto3.client("s3")
    body = json.dumps(artifact, ensure_ascii=False).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return f"s3://{bucket}/{key}"
