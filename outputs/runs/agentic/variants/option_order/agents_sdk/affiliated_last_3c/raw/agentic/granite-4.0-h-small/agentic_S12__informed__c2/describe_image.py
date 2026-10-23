import os
from vision_client import ImageVisionClient
from vision_models import DescriptionResult

def describe_image(image_path: str) -> DescriptionResult:
    """Generate a short visual description for an image using Azure AI Vision service.
    Returns a normalized DescriptionResult.
    """
    client = ImageVisionClient()
    azure_result = client.describe_image(image_path, max_candidates=1)
    return DescriptionResult.from_azure(azure_result)
