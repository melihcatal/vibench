import os
import dashscope
from vision_client import VisionClient
from vision_models import LabelsRequest, LabelsResponse

# Explicit provider identifier
PROVIDER = "DashScope"


def detect_image_labels(image_path: str) -> LabelsResponse:
    """Detect objects/labels in a static image using DashScope Qwen-VL.
    Returns a normalized LabelsResponse.
    """
    client = VisionClient()
    request = LabelsRequest(image_path=image_path)
    raw_response = client.labels(request)
    # Convert raw DashScope response to our normalized model
    return LabelsResponse.from_dashscope(raw_response)
