import base64
import os
from typing import Any, Dict

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def load_azure_vision_client() -> ImageAnalysisClient:
    endpoint = os.environ["AZURE_VISION_ENDPOINT"]
    key = os.environ["AZURE_VISION_KEY"]
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def read_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def image_data_uri(image_path: str) -> str:
    raw = read_image_bytes(image_path)
    encoded = base64.b64encode(raw).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def analyze_image(
    client: ImageAnalysisClient, image_path: str, features: Any
) -> Dict[str, Any]:
    with open(image_path, "rb") as image:
        result = client.analyze(image_data=image, visual_features=features)
    return result.as_dict()


def default_features() -> list:
    return [
        VisualFeatures.CAPTION,
        VisualFeatures.OBJECTS,
        VisualFeatures.READ,
        VisualFeatures.TAGS,
        VisualFeatures.SMART_CROPS,
    ]
