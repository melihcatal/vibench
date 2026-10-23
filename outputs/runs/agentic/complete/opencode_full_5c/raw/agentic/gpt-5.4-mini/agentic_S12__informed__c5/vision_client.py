import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class VisionConfig:
    region_name: Optional[str] = None
    max_labels: int = 10
    min_confidence: float = 75.0
    language: str = "en"


def load_vision_config() -> VisionConfig:
    return VisionConfig(
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        max_labels=int(os.getenv("VISION_MAX_LABELS", "10")),
        min_confidence=float(os.getenv("VISION_MIN_CONFIDENCE", "75")),
        language=os.getenv("VISION_LANGUAGE", "en"),
    )


def rekognition_client(region_name: Optional[str] = None):
    cfg = load_vision_config()
    return boto3.client("rekognition", region_name=region_name or cfg.region_name)


def image_bytes_from_input(image: Any) -> bytes:
    if isinstance(image, bytes):
        return image
    if isinstance(image, str):
        with open(image, "rb") as f:
            return f.read()
    raise TypeError("image must be bytes or a file path")


def as_image_payload(image: Any) -> Dict[str, Any]:
    return {"Bytes": image_bytes_from_input(image)}
