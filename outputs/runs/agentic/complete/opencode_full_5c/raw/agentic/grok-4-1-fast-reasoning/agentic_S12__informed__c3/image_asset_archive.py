import os
import boto3
import json
from typing import Any
from vision_models import VisionAnalysis

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def image_asset_archive(
    image_path: str,
    artifacts: VisionAnalysis,
    bucket_name: str,
    prefix: str = "vision-analysis",
):
    image_key = f"{prefix}/image.jpg"
    s3.upload_file(image_path, bucket_name, image_key)

    artifacts_key = f"{prefix}/artifacts.json"
    artifacts_body = json.dumps(artifacts, indent=2).encode("utf-8")
    s3.put_object(
        Bucket=bucket_name,
        Key=artifacts_key,
        Body=artifacts_body,
        ContentType="application/json",
    )
