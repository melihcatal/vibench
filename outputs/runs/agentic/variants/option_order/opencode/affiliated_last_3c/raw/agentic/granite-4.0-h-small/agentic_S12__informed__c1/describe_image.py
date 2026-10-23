import os
import dashscope
from vision_client import VisionClient
from vision_models import DescriptionRequest, DescriptionResponse

# Explicit provider identifier
PROVIDER = "DashScope"


def describe_image(image_path: str) -> DescriptionResponse:
    """Generate a short visual description of an image using DashScope Qwen-VL.
    Returns a normalized DescriptionResponse.
    """
    client = VisionClient()
    request = DescriptionRequest(image_path=image_path)
    raw_response = client.description(request)
    # Convert raw DashScope response to our normalized model
    return DescriptionResponse.from_dashscope(raw_response)
