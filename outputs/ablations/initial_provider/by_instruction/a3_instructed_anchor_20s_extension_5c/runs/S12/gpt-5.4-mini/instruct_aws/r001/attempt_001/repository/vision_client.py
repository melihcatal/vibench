import base64
import os
from typing import Any, Dict, Optional

import boto3

from vision_models import ImageSource


def _session():
    return boto3.session.Session(region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def rekognition_client():
    return _session().client("rekognition")


def s3_client():
    return _session().client("s3")


def load_image_bytes(source: ImageSource) -> bytes:
    if source.bytes_data is not None:
        return source.bytes_data
    if source.path:
        with open(source.path, "rb") as f:
            return f.read()
    if source.bucket and source.key:
        obj = s3_client().get_object(Bucket=source.bucket, Key=source.key)
        return obj["Body"].read()
    raise ValueError("image source requires path, bytes_data, or bucket/key")


def image_bytes_to_data_uri(content: bytes, mime_type: str = "image/jpeg") -> str:
    encoded = base64.b64encode(content).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(name, default)


def get_provider_config() -> Dict[str, Any]:
    return {
        "aws_region": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "aws_rekognition_endpoint": "rekognition.amazonaws.com",
    }
