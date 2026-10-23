import os
from dataclasses import asdict
from typing import Any, Dict

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from vision_models import ImageAnalysisRequest


def load_azure_vision_config() -> Dict[str, str]:
    return {
        "endpoint": os.environ.get("AZURE_VISION_ENDPOINT", ""),
        "key": os.environ.get("AZURE_VISION_KEY", ""),
    }


def build_image_analysis_client() -> ImageAnalysisClient:
    config = load_azure_vision_config()
    return ImageAnalysisClient(config["endpoint"], AzureKeyCredential(config["key"]))


def read_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def request_to_dict(request: ImageAnalysisRequest) -> Dict[str, Any]:
    return asdict(request)
