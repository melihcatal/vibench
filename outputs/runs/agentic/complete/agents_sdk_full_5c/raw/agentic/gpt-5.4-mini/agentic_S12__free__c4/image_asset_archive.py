from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import boto3


def image_asset_archive(artifact: Dict[str, Any], bucket: str, key: str, *, region_name: str = "us-east-1") -> Dict[str, Any]:
    s3 = boto3.client("s3", region_name=region_name)
    body = json.dumps(artifact, ensure_ascii=False).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return {"bucket": bucket, "key": key, "bytes": len(body)}
