from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from vision_client import load_vision_config


def describe_image(image_url: str) -> str:
    config = load_vision_config()
    client = ImageAnalysisClient(config.endpoint, AzureKeyCredential(config.api_key))
    result = client.analyze_from_url(image_url=image_url, visual_features=["caption"])
    caption = getattr(getattr(result, "caption", None), "text", "")
    return str(caption).strip()
