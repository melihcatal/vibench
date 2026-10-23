from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import get_azure_vision_client
from vision_models import ImageDescription

def describe_image(image_path: str) -> ImageDescription | None:
    """
    Generates a caption for an image using Azure AI Vision.

    Args:
        image_path: The path to the local image file.

    Returns:
        An ImageDescription object containing the caption and confidence score, or None.
    """
    client = get_azure_vision_client()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.CAPTION],
    )

    if result.caption is not None:
        return ImageDescription(
            text=result.caption.text, confidence=result.caption.confidence
        )
    return None
