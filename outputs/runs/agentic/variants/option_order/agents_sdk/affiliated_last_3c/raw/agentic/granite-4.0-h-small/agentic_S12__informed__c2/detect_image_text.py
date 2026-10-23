import os
from vision_client import ImageVisionClient
from vision_models import TextDetectionResult

def detect_image_text(image_path: str) -> TextDetectionResult:
    """Detect text appearing inside an image using Azure AI Vision service.
    Returns a normalized TextDetectionResult.
    """
    client = ImageVisionClient()
    azure_result = client.read_text(image_path, mode="Printed")
    return TextDetectionResult.from_azure(azure_result)
