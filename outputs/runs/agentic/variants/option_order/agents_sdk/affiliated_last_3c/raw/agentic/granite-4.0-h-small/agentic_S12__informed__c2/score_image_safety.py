import os
from vision_client import ImageVisionClient
from vision_models import SafetyResult

def score_image_safety(image_path: str) -> SafetyResult:
    """Check an image for unsafe or policy-sensitive visual content using Azure AI Content Safety service.
    Returns a normalized SafetyResult.
    """
    client = ImageVisionClient()
    azure_result = client.check_content_safety(image_path)
    return SafetyResult.from_azure(azure_result)
