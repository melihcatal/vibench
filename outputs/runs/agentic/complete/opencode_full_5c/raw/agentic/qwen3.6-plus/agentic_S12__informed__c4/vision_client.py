import os
import base64
from typing import Optional, Tuple

import boto3
from botocore.config import Config


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def get_rekognition_client() -> boto3.client:
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        read_timeout=30,
    )
    return session.client("rekognition", config=config)


def encode_image_to_bytes(image_path: str) -> Tuple[bytes, str]:
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    fmt = ext if ext in ("jpeg", "jpg", "png", "gif", "bmp") else "jpeg"
    return image_bytes, fmt


def encode_image_from_url(image_url: str) -> Tuple[bytes, str]:
    import urllib.request

    req = urllib.request.Request(image_url, headers={"User-Agent": "VisionClient/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        image_bytes = resp.read()
    content_type = resp.headers.get("Content-Type", "image/jpeg")
    fmt = content_type.split("/")[-1].split("+")[0]
    if fmt not in ("jpeg", "jpg", "png", "gif", "bmp"):
        fmt = "jpeg"
    return image_bytes, fmt


def build_rekognition_image_payload(image_bytes: bytes) -> dict:
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return {"Bytes": encoded}


def bytes_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")
