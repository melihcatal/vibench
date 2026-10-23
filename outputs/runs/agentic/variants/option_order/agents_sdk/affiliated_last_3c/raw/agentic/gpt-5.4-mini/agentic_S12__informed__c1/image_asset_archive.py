from __future__ import annotations

import json
from typing import Any, Dict

import boto3


def image_asset_archive(bucket: str, key: str, artifact: Dict[str, Any], caption: str) -> Dict[str, str]:
    s3 = boto3.client("s3")
    artifact_key = f"{key}.json"
    caption_key = f"{key}.txt"
    s3.put_object(Bucket=bucket, Key=artifact_key, Body=json.dumps(artifact).encode("utf-8"), ContentType="application/json")
    s3.put_object(Bucket=bucket, Key=caption_key, Body=caption.encode("utf-8"), ContentType="text/plain")
    return {"artifact_key": artifact_key, "caption_key": caption_key}
