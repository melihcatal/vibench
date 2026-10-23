from __future__ import annotations

import json

from vision_client import get_s3_client
from vision_models import ArchiveResult


def image_asset_archive(bucket: str, key: str, artifacts: dict) -> dict:
    s3 = get_s3_client()
    body = json.dumps(artifacts, ensure_ascii=False).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return ArchiveResult(
        provider="amazon-s3", bucket=bucket, key=key, uri=f"s3://{bucket}/{key}"
    ).to_dict()
