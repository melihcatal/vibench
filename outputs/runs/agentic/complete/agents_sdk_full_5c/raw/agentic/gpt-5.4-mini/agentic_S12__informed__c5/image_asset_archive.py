from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import boto3


S3_BUCKET_ENV = "IMAGE_ASSET_ARCHIVE_BUCKET"


def archive_image_analysis(bucket: str, key_prefix: str, metadata: Dict[str, Any], caption: str, image_path: str) -> Dict[str, str]:
    s3 = boto3.client("s3")
    asset_key = f"{key_prefix.rstrip('/')}/image.bin"
    meta_key = f"{key_prefix.rstrip('/')}/analysis.json"
    caption_key = f"{key_prefix.rstrip('/')}/caption.txt"
    s3.upload_file(image_path, bucket, asset_key)
    s3.put_object(Bucket=bucket, Key=meta_key, Body=json.dumps(metadata).encode("utf-8"), ContentType="application/json")
    s3.put_object(Bucket=bucket, Key=caption_key, Body=caption.encode("utf-8"), ContentType="text/plain; charset=utf-8")
    return {"image": asset_key, "metadata": meta_key, "caption": caption_key}
