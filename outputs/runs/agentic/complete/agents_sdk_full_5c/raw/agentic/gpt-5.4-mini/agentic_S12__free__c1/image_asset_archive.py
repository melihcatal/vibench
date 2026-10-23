from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict

import boto3

from vision_models import ArchiveRecord

AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "")
AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def image_asset_archive(image_path: str, caption: str, metadata: Dict[str, object] | None = None) -> str:
    if not AWS_S3_BUCKET:
        raise ValueError("AWS_S3_BUCKET is required")
    s3 = boto3.client("s3", region_name=AWS_REGION)
    path = Path(image_path)
    asset_key = f"image-analysis/{path.stem}.json"
    record = ArchiveRecord(asset_key=asset_key, caption=caption, metadata=metadata or {})
    s3.put_object(Bucket=AWS_S3_BUCKET, Key=asset_key, Body=json.dumps({"caption": record.caption, "metadata": record.metadata}).encode("utf-8"), ContentType="application/json")
    return asset_key
