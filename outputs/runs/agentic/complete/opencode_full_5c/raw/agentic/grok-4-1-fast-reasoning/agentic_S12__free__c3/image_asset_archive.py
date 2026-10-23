import boto3
import json
import os
from os import path as ospath
from dataclasses import asdict
from vision_client import get_s3_bucket
from vision_models import FullVisionAnalysis


def image_asset_archive(
    image_path: str,
    analysis: FullVisionAnalysis,
    bucket: str = None,
    prefix: str = "analysis/",
) -> str:
    if bucket is None:
        bucket = get_s3_bucket()
    key = f"{prefix}{ospath.basename(image_path)}_analysis.json"
    artifacts = {
        "image_path": image_path,
        "analysis": asdict(analysis),
    }
    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=bucket, Key=key, Body=json.dumps(artifacts, indent=2))
    return f"s3://{bucket}/{key}"
