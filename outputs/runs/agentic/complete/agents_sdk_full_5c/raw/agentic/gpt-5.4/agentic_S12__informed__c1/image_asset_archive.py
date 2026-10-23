from __future__ import annotations

import json
import os
from typing import Any

from vision_client import get_boto3_client
from vision_models import ArchiveResult


PROVIDER = "amazon-s3"


def image_asset_archive(bucket: str, key: str, artifact: Any, content_type: str = "application/json") -> ArchiveResult:
    s3 = get_boto3_client("s3")
    body = artifact if isinstance(artifact, (bytes, bytearray)) else json.dumps(artifact, ensure_ascii=False).encode("utf-8")
    if content_type == "application/json" and not key.endswith(".json"):
        key = f"{key}.json"
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    uri = f"s3://{bucket}/{key}"
    return ArchiveResult(provider=PROVIDER, bucket=bucket, key=key, uri=uri)
