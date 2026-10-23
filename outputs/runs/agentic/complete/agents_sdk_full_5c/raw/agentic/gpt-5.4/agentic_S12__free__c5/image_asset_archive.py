from __future__ import annotations

import json
import os
from typing import Any, Mapping

import boto3


S3_BUCKET = os.getenv("ARCHIVE_S3_BUCKET", "image-analysis-archive")
S3_PREFIX = os.getenv("ARCHIVE_S3_PREFIX", "visual-artifacts/")


def image_asset_archive(asset_id: str, analysis_payload: Mapping[str, Any]) -> str:
    s3 = boto3.client("s3")
    key = f"{S3_PREFIX}{asset_id}.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(analysis_payload, ensure_ascii=False, indent=2).encode("utf-8"),
        ContentType="application/json",
    )
    return f"s3://{S3_BUCKET}/{key}"
