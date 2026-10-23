from azure.cognitiveservices.vision.imageanalysis.models import VisualFeatures
from vision_client import get_azure_vision_client


def describe_image(image_url: str) -> str:
    """Generates a short visual description for an image using Azure AI Vision."""
    client = get_azure_vision_client()

    result = client.analyze_from_url(
        image_url=image_url, visual_features=[VisualFeatures.CAPTION]
    )

    if result.caption is not None:
        return result.caption.text
    return "No description generated."
