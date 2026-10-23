from __future__ import annotations

import json
from pathlib import Path

import boto3

S3_BUCKET_ENV = "IMAGE_ASSET_ARCHIVE_BUCKET"


def archive_image_artifacts(bucket: str, key_prefix: str, image_path: str, captions: list[str]) -> dict:
    s3 = boto3.client("s3")
    image_key = f"{key_prefix}/{Path(image_path).name}"
    s3.upload_file(image_path, bucket, image_key)
    captions_key = f"{key_prefix}/captions.json"
    body = json.dumps({"image": image_key, "captions": captions}).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=captions_key, Body=body, ContentType="application/json")
    return {"image_key": image_key, "captions_key": captions_key}
