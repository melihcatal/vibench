import base64
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class VisionConfig:
    endpoint: str
    key: str


def load_config() -> VisionConfig:
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT", "").strip()
    key = os.environ.get("AZURE_VISION_KEY", "").strip()
    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY are required")
    return VisionConfig(endpoint=endpoint, key=key)


@lru_cache(maxsize=1)
def get_client() -> ImageAnalysisClient:
    cfg = load_config()
    return ImageAnalysisClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key))


def image_source_from_path(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def image_source_from_base64(image_b64: str) -> bytes:
    return base64.b64decode(image_b64)


def feature_set_for_labels():
    return [VisualFeatures.TAGS, VisualFeatures.OBJECTS]


def feature_set_for_description():
    return [VisualFeatures.CAPTION]


def feature_set_for_text():
    return [VisualFeatures.READ]


def feature_set_for_safety():
    return [VisualFeatures.DENSE_CAPTIONS, VisualFeatures.OBJECTS, VisualFeatures.TAGS]
