import json
import os

import boto3

from vision_client import load_config


def image_asset_archive(asset_name, analysis, caption):
    cfg = load_config()
    bucket = cfg.storage_bucket or os.getenv("AWS_S3_BUCKET")
    if not bucket:
        raise RuntimeError("AWS_S3_BUCKET is required")
    s3 = boto3.client("s3", region_name=cfg.storage_region)
    body = json.dumps(
        {"asset_name": asset_name, "analysis": analysis, "caption": caption},
        ensure_ascii=False,
    ).encode("utf-8")
    key = f"image-archive/{asset_name}.json"
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return {"bucket": bucket, "key": key}
