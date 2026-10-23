
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

from vision_client import get_azure_vision_client
from vision_models import ImageDescription

def describe_image(image_url: str) -> ImageDescription:
    """
    Generates a description for an image using Azure AI Vision.
    """
    client = get_azure_vision_client()
    
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=["caption", "tags"]
    )

    description = ""
    if result.caption is not None:
        description = result.caption.text

    tags = []
    if result.tags is not None:
        tags = [tag.name for tag in result.tags]
        
    return ImageDescription(description=description, tags=tags)
