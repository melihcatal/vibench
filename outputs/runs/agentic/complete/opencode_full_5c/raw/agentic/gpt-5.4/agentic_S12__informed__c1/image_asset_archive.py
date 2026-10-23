from __future__ import annotations

import json
import os
from typing import Any, Dict

import boto3


def image_asset_archive(
    bucket: str, object_prefix: str, artifacts: Dict[str, Any]
) -> dict:
    client = boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1",
    )
    uploaded = []
    for name, payload in artifacts.items():
        key = f"{object_prefix.rstrip('/')}/{name}.json"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        client.put_object(
            Bucket=bucket, Key=key, Body=body, ContentType="application/json"
        )
        uploaded.append({"bucket": bucket, "key": key, "provider": "amazon-s3"})
    return {"provider": "amazon-s3", "bucket": bucket, "objects": uploaded}
