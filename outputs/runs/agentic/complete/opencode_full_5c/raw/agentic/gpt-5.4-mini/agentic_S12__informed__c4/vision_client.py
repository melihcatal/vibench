import os
from typing import Any

import boto3


def get_rekognition_client() -> Any:
    return boto3.client("rekognition")


def get_region() -> str:
    return os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def read_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as handle:
        return handle.read()


def get_bucket_name() -> str:
    return os.getenv("IMAGE_ARCHIVE_BUCKET", "")


def get_s3_client() -> Any:
    return boto3.client("s3", region_name=get_region())
