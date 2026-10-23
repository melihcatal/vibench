import os
from typing import Dict

import boto3

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
S3_REGION = os.getenv("AWS_REGION", "us-east-1")


def image_asset_archive(key: str, payload: Dict[str, str]) -> None:
    s3 = boto3.client("s3", region_name=S3_REGION, endpoint_url=S3_ENDPOINT_URL)
    s3.put_object(Bucket=S3_BUCKET_NAME, Key=key, Body=str(payload).encode("utf-8"), ContentType="application/json")
