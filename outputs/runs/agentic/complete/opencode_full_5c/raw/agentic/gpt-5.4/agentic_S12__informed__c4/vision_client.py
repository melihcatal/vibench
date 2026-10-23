from __future__ import annotations

import base64
import json
import os
from typing import Any

import boto3
from openai import OpenAI

from vision_models import ImageInput


def load_image_bytes(image: ImageInput) -> bytes:
    if image.image_bytes is not None:
        return image.image_bytes
    if not image.image_path:
        raise ValueError("image_path or image_bytes is required")
    with open(image.image_path, "rb") as handle:
        return handle.read()


def to_data_url(image: ImageInput) -> str:
    payload = base64.b64encode(load_image_bytes(image)).decode("utf-8")
    return f"data:{image.mime_type};base64,{payload}"


def create_rekognition_client(region_name: str | None = None):
    return boto3.client(
        "rekognition",
        region_name=region_name
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1",
    )


def create_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_s3_client(region_name: str | None = None):
    return boto3.client(
        "s3",
        region_name=region_name
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1",
    )


def json_dumps(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True)
