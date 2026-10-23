from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from vision_models import ImageAnalysisRequest


@dataclass
class VisionConfig:
    endpoint: str
    key: str


def load_config() -> VisionConfig:
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT", "")
    key = os.environ.get("AZURE_VISION_KEY", "")
    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY are required")
    return VisionConfig(endpoint=endpoint, key=key)


def create_client(config: Optional[VisionConfig] = None) -> ImageAnalysisClient:
    config = config or load_config()
    return ImageAnalysisClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key))


def image_to_data_uri(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def request_payload(request: ImageAnalysisRequest) -> Dict[str, Any]:
    return {
        "image_path": request.image_path,
        "image_url": request.image_url,
        "language": request.language or "en",
        "max_results": request.max_results,
        "threshold": request.threshold,
    }
