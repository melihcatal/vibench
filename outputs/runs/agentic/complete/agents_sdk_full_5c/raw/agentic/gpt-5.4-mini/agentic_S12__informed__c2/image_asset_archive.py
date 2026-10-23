from __future__ import annotations

import json
import os
from typing import Dict

import boto3

S3_BUCKET = os.getenv("IMAGE_ASSET_ARCHIVE_BUCKET", "")


def archive_image_artifacts(object_key: str, data: Dict):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=S3_BUCKET, Key=object_key, Body=json.dumps(data).encode("utf-8"), ContentType="application/json")
    return {"bucket": S3_BUCKET, "key": object_key}
