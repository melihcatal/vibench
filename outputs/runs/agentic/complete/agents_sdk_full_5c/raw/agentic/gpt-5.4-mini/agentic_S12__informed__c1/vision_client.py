from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from vision_models import ImageDescription, LabelResult, SafetyResult, TextResult


@dataclass
class VisionConfig:
    endpoint: str
    key: str
    api_version: str = "2024-02-01"


def load_config() -> VisionConfig:
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT", "").strip()
    key = os.environ.get("AZURE_VISION_KEY", "").strip()
    if not endpoint or not key:
        raise RuntimeError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY are required")
    return VisionConfig(endpoint=endpoint, key=key)


def build_client(config: Optional[VisionConfig] = None) -> ImageAnalysisClient:
    config = config or load_config()
    return ImageAnalysisClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key))


def read_image_bytes(image_path: str) -> bytes:
    return Path(image_path).read_bytes()


def read_image_data_url(image_path: str) -> str:
    data = read_image_bytes(image_path)
    encoded = base64.b64encode(data).decode("ascii")
    suffix = Path(image_path).suffix.lower().lstrip(".") or "jpeg"
    return f"data:image/{suffix};base64,{encoded}"


def extract_labels(result: Any) -> list[LabelResult]:
    tags = getattr(result, "tags", None) or []
    return [LabelResult(name=str(tag.name), score=float(tag.confidence)) for tag in tags]


def extract_description(result: Any) -> ImageDescription:
    captions = getattr(result, "caption", None)
    if captions and getattr(captions, "text", None):
        return ImageDescription(caption=str(captions.text), confidence=float(getattr(captions, "confidence", 0.0)))
    return ImageDescription(caption="", confidence=None)


def extract_text(result: Any) -> list[TextResult]:
    blocks = []
    read = getattr(result, "read", None)
    if read and getattr(read, "blocks", None):
        for block in read.blocks:
            for line in getattr(block, "lines", []) or []:
                blocks.append(TextResult(text=str(line.text), confidence=float(getattr(line, "confidence", 0.0))))
    return blocks


def extract_safety(result: Any) -> SafetyResult:
    moderation = getattr(result, "moderation", None)
    if moderation:
        categories = []
        for key, value in moderation.__dict__.items():
            if bool(value):
                categories.append(str(key))
        return SafetyResult(unsafe=bool(categories), categories=categories, score=None)
    return SafetyResult(unsafe=False, categories=[], score=None)
