from __future__ import annotations

import json
from typing import Any, Dict

import boto3

from vision_client import AWS_S3_HOST, get_s3_bucket_name


def image_asset_archive(
    asset_id: str, artifact_bundle: Dict[str, Any]
) -> Dict[str, str]:
    bucket = get_s3_bucket_name()
    s3 = boto3.client("s3", endpoint_url=f"https://{AWS_S3_HOST}")
    key = f"visual-analysis/{asset_id}.json"
    payload = json.dumps(artifact_bundle, ensure_ascii=False).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=payload, ContentType="application/json")
    return {
        "provider": "aws-s3",
        "bucket": bucket,
        "key": key,
        "uri": f"s3://{bucket}/{key}",
    }
