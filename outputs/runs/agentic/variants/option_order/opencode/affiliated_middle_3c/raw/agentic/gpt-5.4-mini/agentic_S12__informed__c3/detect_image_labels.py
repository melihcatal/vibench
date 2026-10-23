from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from vision_client import load_vision_config
from vision_models import normalize_labels


def detect_image_labels(image_url: str):
    config = load_vision_config()
    client = ImageAnalysisClient(config.endpoint, AzureKeyCredential(config.api_key))
    result = client.analyze_from_url(image_url=image_url, visual_features=["tags"])
    return normalize_labels([{"name": tag.name} for tag in getattr(result, "tags", [])])
