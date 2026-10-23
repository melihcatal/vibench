from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import boto3
from openai import OpenAI

from vision_models import ImageInput


def load_image_bytes(image: ImageInput | str) -> bytes:
    if isinstance(image, str):
        return Path(image).read_bytes()
    if image.image_path:
        return Path(image.image_path).read_bytes()
    raise ValueError("image_path is required for byte-based providers")


def image_location(image: ImageInput | str) -> ImageInput:
    if isinstance(image, str):
        return ImageInput(image_path=image)
    return image


def rekognition_client() -> Any:
    region_name = (
        os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    )
    return boto3.client("rekognition", region_name=region_name)


def translate_client() -> Any:
    region_name = (
        os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    )
    return boto3.client("translate", region_name=region_name)


def s3_client() -> Any:
    region_name = (
        os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    )
    return boto3.client("s3", region_name=region_name)


def openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def to_openai_input_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)
