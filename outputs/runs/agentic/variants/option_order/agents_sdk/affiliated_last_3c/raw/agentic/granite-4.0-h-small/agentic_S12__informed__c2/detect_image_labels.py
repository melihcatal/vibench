import os
from vision_client import ImageVisionClient
from vision_models import LabelResult

def detect_image_labels(image_path: str) -> LabelResult:
    """Detect labels/objects in a static image using Azure AI Vision service.
    Returns a normalized LabelResult.
    """
    client = ImageVisionClient()
    # Azure Vision SDK provides image analysis
    azure_result = client.analyze_image(image_path, features=["Categories", "Tags", "Description", "Faces"])
    # Normalize to our local model
    return LabelResult.from_azure(azure_result)
