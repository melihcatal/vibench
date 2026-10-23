import base64
import os
from pathlib import Path
from typing import Any, Dict, Optional

import boto3

from vision_models import VisionImageInput


AWS_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def load_image_input(image_path: str) -> VisionImageInput:
    path = Path(image_path)
    return VisionImageInput(image_path=str(path), image_bytes=path.read_bytes())


def rekognition_client():
    return boto3.client("rekognition", region_name=AWS_REGION)


def image_bytes_payload(image: VisionImageInput) -> Dict[str, Any]:
    if image.image_bytes is None:
        image.image_bytes = Path(image.image_path).read_bytes()
    return {"Bytes": image.image_bytes}


def image_base64(image: VisionImageInput) -> str:
    if image.image_bytes is None:
        image.image_bytes = Path(image.image_path).read_bytes()
    return base64.b64encode(image.image_bytes).decode("utf-8")


def get_client_metadata() -> Dict[str, Any]:
    return {"provider": "aws", "service": "rekognition", "region": AWS_REGION}
