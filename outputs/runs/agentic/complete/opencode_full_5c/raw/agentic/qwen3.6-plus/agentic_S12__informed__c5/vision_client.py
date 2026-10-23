import os
import io
from typing import Optional, Tuple
import boto3
from botocore.exceptions import ClientError


REKOGNITION_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")


def get_rekognition_client(region: Optional[str] = None):
    region_name = region or REKOGNITION_REGION
    return boto3.client(
        "rekognition",
        region_name=region_name,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def load_image_from_url(url: str) -> bytes:
    import urllib.request

    with urllib.request.urlopen(url) as response:
        return response.read()


def load_image_from_path(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def prepare_image_bytes(
    image_url: Optional[str] = None,
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> bytes:
    if image_bytes is not None:
        return image_bytes
    if image_path is not None:
        return load_image_from_path(image_path)
    if image_url is not None:
        return load_image_from_url(image_url)
    raise ValueError(
        "No image source provided. Supply image_url, image_path, or image_bytes."
    )


def call_rekognition_detect_labels(client, image_bytes: bytes) -> dict:
    response = client.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=50,
        MinConfidence=50.0,
    )
    return response


def call_rekognition_detect_text(client, image_bytes: bytes) -> dict:
    response = client.detect_text(
        Image={"Bytes": image_bytes},
    )
    return response


def call_rekognition_detect_moderation(client, image_bytes: bytes) -> dict:
    response = client.detect_moderation_labels(
        Image={"Bytes": image_bytes},
        MinConfidence=50.0,
    )
    return response


def validate_aws_credentials() -> bool:
    return bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)
