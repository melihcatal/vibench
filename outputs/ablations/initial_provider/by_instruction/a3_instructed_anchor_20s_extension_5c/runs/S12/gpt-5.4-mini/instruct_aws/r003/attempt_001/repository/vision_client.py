import base64
import os
from pathlib import Path
from typing import Any, Dict, List

import boto3

from vision_models import normalize_labels, normalize_text_lines


AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def _rekognition_client():
    return boto3.client("rekognition", region_name=AWS_REGION)


def _load_bytes(image_path: str) -> bytes:
    return Path(image_path).read_bytes()


def detect_labels(image_path: str, max_labels: int = 10) -> List[Dict[str, Any]]:
    response = _rekognition_client().detect_labels(Image={"Bytes": _load_bytes(image_path)}, MaxLabels=max_labels)
    return normalize_labels(response.get("Labels", []))


def describe_image(image_path: str, max_labels: int = 5) -> str:
    labels = detect_labels(image_path, max_labels=max_labels)
    names = [label["name"] for label in labels[:3] if label["name"]]
    return ", ".join(names) if names else "Image"


def detect_text(image_path: str) -> List[str]:
    response = _rekognition_client().detect_text(Image={"Bytes": _load_bytes(image_path)})
    texts = [item.get("DetectedText", "") for item in response.get("TextDetections", []) if item.get("Type") == "LINE"]
    return normalize_text_lines(texts)


def detect_safe_search(image_path: str) -> Dict[str, Any]:
    response = _rekognition_client().detect_moderation_labels(Image={"Bytes": _load_bytes(image_path)})
    return {"labels": response.get("ModerationLabels", []), "sensitive": bool(response.get("ModerationLabels"))}
