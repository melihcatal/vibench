import os
from dataclasses import dataclass
from typing import Optional

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class VisionConfig:
    endpoint: str
    key: str


def load_config() -> VisionConfig:
    endpoint = os.getenv("AZURE_VISION_ENDPOINT", "").strip()
    key = os.getenv("AZURE_VISION_KEY", "").strip()
    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY are required")
    return VisionConfig(endpoint=endpoint, key=key)


def build_client(config: Optional[VisionConfig] = None) -> ImageAnalysisClient:
    cfg = config or load_config()
    return ImageAnalysisClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key))
