import base64
import os
from dataclasses import asdict
from typing import Any, Dict, Optional

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_models import VisionImageInput


def get_azure_vision_client() -> ImageAnalysisClient:
    endpoint = os.environ["AZURE_VISION_ENDPOINT"]
    key = os.environ["AZURE_VISION_KEY"]
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def load_image_input(
    image_path: str, image_url: Optional[str] = None
) -> VisionImageInput:
    return VisionImageInput(image_path=image_path, image_url=image_url)


def image_source_kwargs(image: VisionImageInput) -> Dict[str, Any]:
    if image.image_url:
        return {"image_url": image.image_url}
    with open(image.image_path, "rb") as f:
        return {"image_data": f.read()}


def to_data_uri(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"
