from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import boto3


AWS_PROVIDER = "aws-s3"
S3_API_HOST = "s3.amazonaws.com"


def image_asset_archive(*, bucket: str, key_prefix: str, artifact: Dict[str, Any], image_bytes: Optional[bytes] = None) -> Dict[str, str]:
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    results: Dict[str, str] = {}

    metadata_key = f"{key_prefix.rstrip('/')}/analysis.json"
    s3.put_object(
        Bucket=bucket,
        Key=metadata_key,
        Body=json.dumps(artifact, ensure_ascii=False).encode("utf-8"),
        ContentType="application/json",
    )
    results["analysis"] = f"s3://{bucket}/{metadata_key}"

    caption = artifact.get("description") or artifact.get("caption")
    if caption:
        caption_key = f"{key_prefix.rstrip('/')}/caption.txt"
        s3.put_object(
            Bucket=bucket,
            Key=caption_key,
            Body=str(caption).encode("utf-8"),
            ContentType="text/plain; charset=utf-8",
        )
        results["caption"] = f"s3://{bucket}/{caption_key}"

    if image_bytes is not None:
        image_key = f"{key_prefix.rstrip('/')}/source-image.jpg"
        s3.put_object(
            Bucket=bucket,
            Key=image_key,
            Body=image_bytes,
            ContentType="image/jpeg",
        )
        results["image"] = f"s3://{bucket}/{image_key}"

    return results
