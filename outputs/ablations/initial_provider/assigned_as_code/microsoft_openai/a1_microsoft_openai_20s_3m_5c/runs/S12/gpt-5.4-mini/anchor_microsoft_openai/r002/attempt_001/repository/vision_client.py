import os
from typing import Any, Dict

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_models import get_image_bytes, make_config


def build_azure_vision_client(config: Dict[str, Any]):
    config = make_config(config)
    endpoint = config.get('endpoint') or os.environ['AZURE_VISION_ENDPOINT']
    api_key = config.get('api_key') or os.environ['AZURE_VISION_API_KEY']
    return ImageAnalysisClient(endpoint, AzureKeyCredential(api_key))


def analyze_image(payload: Dict[str, Any], config: Dict[str, Any], visual_features):
    image_bytes = get_image_bytes(payload)
    with build_azure_vision_client(config) as client:
        return client.analyze(image_data=image_bytes, visual_features=visual_features)


def default_text_features():
    return [VisualFeatures.READ]
